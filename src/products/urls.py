from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from .views import ProductAddView, ProductDownloadView, ProductUpdateView, ProductDetailView, ProductListView, ExampleView, VariationListView

urlpatterns = [
    # Examples:
    #url(r'^$', 'newsletter.views.home', name='home'),
    url(r'^$', ProductListView.as_view(), name='products'),
    url(r'^(?P<pk>\d+)/$', ProductDetailView.as_view(), name='product_detail'),
    #url(r'^(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='product_detail_slug'),
    url(r'^(?P<pk>\d+)/inventory/$', VariationListView.as_view(), name='product_inventory'),
    #url(r'^create/$', 'products.views.create_view', name='create_view'),    
    #url(r'^(?P<pk>\d+)/edit/$', 'products.views.edit_view', name='edit_view'), 
    url(r'^ask/$', ProductAddView.as_view(), name='add_view'),
    url(r'^(?P<pk>\d+)/download/$', ProductDownloadView.as_view(), name='download'),
    url(r'^(?P<slug>[\w-]+)/download/$', ProductDownloadView.as_view(), name='download_slug'), 
    url(r'^(?P<pk>\d+)/update/$', ProductUpdateView.as_view(), name='update_view'),
    url(r'^(?P<slug>[\w-]+)/update/$', ProductUpdateView.as_view(), name='update_view'), 
    # viewing an example
    url(r'^example/$', ExampleView.as_view(), name='example'),
    #url(r'^(?P<id>\d+)', 'product.views.product_detail', name='product_detail_view_func'),
]