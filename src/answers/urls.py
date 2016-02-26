from django.conf.urls import include, url
from django.contrib import admin

from products.views import (
		ProductAddView,
		ProductUpdateView,
		SellerProductListView,
        ProductAddView
	)


from .views import (
        SellerDashboard,
        SellerProductDetailRedirectView,
        SellerTransactionListView,

        )

urlpatterns = [
    url(r'^$', SellerDashboard.as_view(), name='dashboard'),
    url(r'^transactions/$', SellerTransactionListView.as_view(), name='transactions'),
    url(r'^products/$', SellerProductListView.as_view(), name='product_list'), #sellers:product_list
    # url(r'^products/(?P<pk>\d+)/$', SellerProductDetailRedirectView.as_view()),
    # url(r'^products/(?P<pk>\d+)/edit/$', ProductUpdateView.as_view(), name='product_edit'),
    url(r'^products/ask/$', ProductAddView.as_view(), name='product_create'),
]   