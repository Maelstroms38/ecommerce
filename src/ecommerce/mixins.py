from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404


from .decorators import ajax_required

class StaffRequiredMixin(object):
	@classmethod
	def as_view(self, *args, **kwargs):
		view = super(StaffRequiredMixin, self).as_view(*args, **kwargs)
		return login_required(view)

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_staff:
			return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)
		else:
			raise Http404

class LoginRequiredMixin(object):
	@classmethod
	def as_view(self, *args, **kwargs):
		view = super(LoginRequiredMixin, self).as_view(*args, **kwargs)
		return login_required(view)

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class MultiSlugMixin(object):
	model = None
	def get_object(self, *args, **kwargs):
		slug = self.kwargs.get("slug")
		ModelClass = self.model
		if slug is not None:
			try:
				obj = get_object_or_404(ModelClass, slug=slug)
			except ModelClass.MultipleObjectsReturned:
				obj = ModelClass.objects.filter(slug=slug).order_by("-title").first()
		else:
			obj = super(MultiSlugMixin, self).get_object(*args, **kwargs)
		return obj

class SubmitMixin(object):
	submit_btn = None
	submit_btn2 = None
	title = None
	def get_context_data(self, *args, **kwargs):
		context = super(SubmitMixin, self).get_context_data(*args, **kwargs)
		context["submit_btn"] = self.submit_btn
		context["submit_btn2"] = self.submit_btn2
		context["title"] = self.title
		return context

class AjaxRequiredMixin(object):
	@method_decorator(ajax_required)
	def dispatch(self, request, *args, **kwargs):
		return super(AjaxRequiredMixin, self).dispatch(request, *args, **kwargs)

