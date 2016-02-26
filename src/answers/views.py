from django.shortcuts import render
from django.views.generic import View
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

from billing.models import Order
from .mixins import LoginRequiredMixin
from products.models import Product

from .forms import NewSellerForm
from .mixins import SellerAccountMixin
from .models import AnswerAccount

class SellerProductDetailRedirectView(RedirectView):
    permanent = True
    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Product, pk=kwargs['pk'])
        return obj.get_absolute_url()




class SellerTransactionListView(SellerAccountMixin, ListView):
    model = Order
    template_name = "answers/transaction_list_view.html"

    def get_queryset(self):
        return self.get_transactions()



class SellerDashboard(SellerAccountMixin, FormMixin, View):
    form_class = NewSellerForm
    success_url = "/answers/"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        apply_form = self.get_form() #NewSellerForm()
        account = AnswerAccount.objects.filter(user=self.request.user)
        exists = account.exists()
        active = None

        # context = {
        #   "apply_form":apply_form,
        #   "account": account,
        #   "active": active,
        #   "exists": exists,
        # }
        context = {}

        if exists:
            account = account.first()
            active = account.active

        #if no account exists, show form
        #if exists and no active, show pending
        #if exists and active, show dashboard data
        if not exists and not active:
            context["title"] = "Apply for Account"
            context["apply_form"] = apply_form
        elif exists and not active:
            context["title"] = "Account Pending"
        elif exists and active:
            context["title"] = "Answers Dashboard"
            # context["products"] = self.get_products()
        else:
            pass
        
        return render(request, "answers/dashboard.html", context)

    def form_valid(self, form):
        valid_data = super(SellerDashboard, self).form_valid(form)
        obj = AnswerAccount.objects.create(user=self.request.user)
        return valid_data