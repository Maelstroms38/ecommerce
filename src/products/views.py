import os
from django.conf import settings
from mimetypes import guess_type
from django.core.exceptions import ImproperlyConfigured
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.generic import View, TemplateView
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from .forms import VariationInventoryFormSet, ProductModelForm, ProductFilterForm, CategoryForm
from django.contrib import messages
from answers.mixins import SellerAccountMixin
from products.mixins import ProductManagerMixin
from django_filters import FilterSet, CharFilter, NumberFilter
import json
from ecommerce.mixins import (
            LoginRequiredMixin,
            StaffRequiredMixin,
            MultiSlugMixin, 
            SubmitMixin,
            AjaxRequiredMixin
            )

# Create your views here.

from .models import Product, Variation, Category, ProductManager

class CategoryListView(ListView):
	model = Category
	queryset = Category.objects.all()
	template_name = "products/product_list.html"

class CategoryDetailView(DetailView):
	model = Category

	def get_context_data(self, *args, **kwargs):
		context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
		obj = self.get_object()
		product_set = obj.product_set.all()
		default_products = obj.default_category.all()
		products = (product_set | default_products).distinct() #combines default category
		context["products"] = products
		return context

class VariationListView(StaffRequiredMixin, ListView):
	model = Variation
	queryset = Variation.objects.all()

	def get_context_data(self, *args, **kwargs):
		context = super(VariationListView, self).get_context_data(*args, **kwargs)
		context["formset"] = VariationInventoryFormSet(queryset=self.get_queryset())
		return context

	def get_queryset(self, *args, **kwargs):
		product_pk = self.kwargs.get("pk")
		if product_pk:
			product = get_object_or_404(Product, pk=product_pk)
			queryset = Variation.objects.filter(product=product)
		return queryset

	def post(self, request, *args, **kwargs):
		#
		formset = VariationInventoryFormSet(request.POST, request.FILES)
		print request.POST
		if formset.is_valid():
			formset.save(commit=False)
			for form in formset:
				new_item = form.save(commit=False)
				if new_item.title:								
					product_pk = self.kwargs.get("pk")						
					product = get_object_or_404(Product, pk=product_pk)
					new_item.product = product	
					new_item.save()		
				
			messages.success(request, "Your inventory and pricing has been updated.")
			return redirect("products")
		raise Http404

class ProductFilter(FilterSet):
	title = CharFilter(name='title', lookup_type='icontains', distinct=True)
	category = CharFilter(name='categories__title', lookup_type='icontains', distinct=True)
	category_id = CharFilter(name='categories__id', lookup_type='icontains', distinct=True)
	min_price = NumberFilter(name='variation__price', lookup_type='gte', distinct=True) # (some_price__gte=somequery)
	max_price = NumberFilter(name='variation__price', lookup_type='lte', distinct=True)
	class Meta:
		model = Product
		fields = [
			'min_price',
			'max_price',
			'category',
			'title',
			'description',
		]
def product_list(request):
	qs = Product.objects.all()
	ordering = request.GET.get("ordering")
	if ordering:
		qs = Product.objects.all().order_by(ordering)
	f = ProductFilter(request.GET, queryset=qs)
	return render(request, "products/product_list.html", {"object_list": f })

class FilterMixin(object):
	filter_class = None
	search_ordering_param = "ordering"

	def get_queryset(self, *args, **kwargs):
		try:
			qs = super(FilterMixin, self).get_queryset(*args, **kwargs)
			return qs
		except:
			raise ImproperlyConfigured("You must have a queryset in order to use the FilterMixin")

	def get_context_data(self, *args, **kwargs):
		context = super(FilterMixin, self).get_context_data(*args, **kwargs)
		qs = self.get_queryset()
		ordering = self.request.GET.get(self.search_ordering_param)
		if ordering:
			qs = qs.order_by(ordering)
		filter_class = self.filter_class
		if filter_class:
			f = filter_class(self.request.GET, queryset=qs)
			context["object_list"] = f
		return context

class ProductListView(FilterMixin, ListView):
	model = Product
	queryset = Product.objects.all()
	filter_class = ProductFilter


	def get_context_data(self, *args, **kwargs):
		context = super(ProductListView, self).get_context_data(*args, **kwargs)
		context["now"] = timezone.now()
		context["query"] = self.request.GET.get("q") #None
		context["filter_form"] = ProductFilterForm(data=self.request.GET or None)
		return context

	def get_queryset(self, *args, **kwargs):
		qs = super(ProductListView, self).get_queryset(*args, **kwargs)
		query = self.request.GET.get("q")
		if query:
			qs = self.model.objects.filter(
				Q(title__icontains=query) |
				Q(description__icontains=query)
				)
			try:
				qs2 = self.model.objects.filter(
					Q(price=query)
				)
				qs = (qs | qs2).distinct()
			except:
				pass
		return qs

class SellerProductListView(SellerAccountMixin, ListView):
	model = Product
	template_name = "answers/product_list_view.html"

	def get_queryset(self, *args, **kwargs):
		qs = super(SellerProductListView, self).get_queryset(*args, **kwargs)
		qs = qs.filter(seller=self.get_account())
		query = self.request.GET.get("q")
		if query: #searches for title, desc, price
			qs = self.model.objects.filter(
				Q(title__icontains=query) |
				Q(description__icontains=query)
				)
			try:
				qs2 = self.model.objects.filter(
				Q(price=query)
				)
				qs = (qs | qs2).distinct()
			except:
				pass
		return qs

class ProductDownloadView(MultiSlugMixin, DetailView):
	model = Product

	def get(self, request, *args, **kwargs):
		obj = self.get_object()
		if request.user.is_authenticated():
			filepath = os.path.join(settings.MEDIA_URL, obj.media.path)
			guessed_type = guess_type(filepath)[0]
			wrapper = FileWrapper(file(filepath))
			mimetype = 'application/force-download'
			if guessed_type:
				mimetype = guessed_type
			response = HttpResponse(wrapper, content_type=mimetype)
			
			if not request.GET.get("preview"):
				response["Content-Disposition"] = "attachment; filename=%s" %(obj.media.name)
			
			response["X-SendFile"] = str(obj.media.name)
			return response
		else:
			messages.success(request, "Please login to continue.")
			return redirect("products")

class ProductAddView(ProductManagerMixin, SubmitMixin, CreateView):
	model = Product
	form_class = ProductModelForm
	template_name = "products/form.html"
	success_url = "/products/"
	submit_btn = "Ask For Free"
	submit_btn2 = "Ask Premium"
	title = "Ask"

	def form_valid(self, form, *args, **kwargs):
		# user = self.request.user
		# form.instance.user = user
		# seller = self.get_account()
		# form.instance.seller = seller
		valid_data = super(ProductAddView, self).form_valid(form)
		return valid_data

class CategorySelectFormView(FormView):
	form_class = CategoryForm
	template_name = "products/form.html"

	def get_form(self, *args, **kwargs):
		formcat = super(CategorySelectFormView, self).get_form(*args, **kwargs)
		# form.fields("categories").queryset = Category.objects.filter(
		# 	# user=self.request.user
		# 	) 
		return formcat
	def form_valid(self, *args, **kwargs):
		formcat = super(CategorySelectFormView, self).form_valid(*args, **kwargs)
		return formcat

class ProductUpdateView(ProductManagerMixin, SubmitMixin, MultiSlugMixin, UpdateView):
	model = Product
	form_class = ProductModelForm
	template_name = "products/form.html"
	success_url = "/products/"
	submit_btn = "Update"
	title = "Update"

class ProductDetailView(MultiSlugMixin, DetailView):
	model = Product
	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
		instance = self.get_object()
		context["related"] = Product.objects.get_related(instance)
		return context

def product_detail_view_func(request, id):
	product_instance = get_object_or_404(Product, id=id)

	try:
		product_instance = Product.objects.get(id=id)
	except Product.DoesNotExist:
		raise Http404
	except:
		raise Http404

	template = "products/product_detail.html"
	context = {
		"object": product_instance
	}
	return render(request, template, context)

def create_view(request): 
	form = ProductModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		print form.cleaned_data.get("publish")
		instance = form.save(commit=False)
		instance.sale_price = instance.price
		instance.save()
	template = "form.html"
	context = {
			"form": form,
			"submit_btn": "Create Product"
		}
	return render(request, template, context)


def edit_view(request, object_id=None):					
	product = get_object_or_404(Product, id=object_id)
	form = ProductModelForm(request.POST or None, instance=Product)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Your Question has been saved.")
		# data = form.cleaned_data
		# title = data.get("title")
		# description = data.get("description")
		# #price = data.get("price")
		# new_obj = Product.objects.create(title=title, description=description)
	template = "products/update_view.html"
	context = {
		"form": form,
		"object": product,
	}
	return render(request, template, context)

def detail_slug_view(request, slug=None):
	product = Product.objects.get(slug=slug)
	try:
		product = get_object_or_404(Product, slug=slug)
	except Product.MultipleObjectsReturned:
		product = Product.objects.filter(slug=slug).order_by("-title").first()
		template = "products/product_detail.html"
		context = {
			"object": product
		}
		return render(request, template, context)

class ExampleView(TemplateView):
    template_name = "products/example.html"

    def get_context_data(self, **kwargs):
        context = super(ExampleView, self).get_context_data(**kwargs)
        if self.request.GET.get('id'):
	        example = Example.objects.get(id=self.request.GET.get["id"]).all()
	       	context["title"] = example.title
	       	context["content"] = example.content
	       	context["link"] = example.link
       	else:
       		print "no example"
        return context