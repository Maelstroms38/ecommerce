from django.conf import settings
from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.contrib import admin
from carts.views import CartView, ItemCountView, CheckoutView, FinalizeCheckoutView
from billing.views import AddressSelectFormView, UserAddressCreateView, OrderList, OrderDetail
import answers.views
import os

urlpatterns = [
    # Examples:
    url(r'^$', 'newsletter.views.home', name='home'),
    url(r'^contact/$', 'newsletter.views.contact', name='contact'),
    url(r'^about/$', 'ecommerce.views.about', name='about'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^products/', include('products.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^categories/', include('products.urls_categories')),
    url(r'^cart/$', CartView.as_view(), name='cart'),
    url(r'^orders/$', OrderList.as_view(), name='orders'),
    url(r'^orders/(?P<pk>\d+)/$', OrderDetail.as_view(), name='order_detail'),
    url(r'^cart/count/$', ItemCountView.as_view(), name='item_count'),
    url(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
    url(r'^checkout/address/$', AddressSelectFormView.as_view(), name='order_address'),
    url(r'^checkout/address/add/$', UserAddressCreateView.as_view(), name='user_address_create'),
    url(r'^checkout/final/$', FinalizeCheckoutView.as_view(), name='checkout_final'),
    url(r'^payments/', include('djstripe.urls', namespace="djstripe")),
    
    # url(r'^answers/', include("answers.urls", namespace='answers')),
    # url(r'^questions/$', questions.views.IndexView.as_view(), name='index'),
    # url(r'^questions/(?P<pk>[0-9]+)/$', questions.views.DetailView.as_view(), name='detail'),
    # url(r'^questions/(?P<pk>[0-9]+)/results/$', questions.views.ResultsView.as_view(), name='results'),
    # url(r'^questions/(?P<question_id>[0-9]+)/vote/$', questions.views.vote, name='vote'),
    # url(r'^questions/create/$', questions.views.CreateQuestionView.as_view(), name='create'),
    # url(r'^questions/edit/(?P<pk>\d+)/$', questions.views.EditQuestionView.as_view(), name='edit'),
]

# if settings.DEBUG:
# 	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# 	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG: 
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
if not settings.DEBUG:
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'