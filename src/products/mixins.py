from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import get_object_or_404
from answers.mixins import SellerAccountMixin

class ProductManagerMixin(object):
	def get_object(self, *args, **kwargs):
		# seller = self.get_account()
		obj = super(ProductManagerMixin, self).get_object(*args, **kwargs)
		return obj
		# try:
		# 	obj.seller  == seller
		# except:
		# 	raise Http404

		# if obj.seller == seller:
		# 	return obj
		# else:
		# 	raise Http404
