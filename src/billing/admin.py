from django.contrib import admin

from .models import Order, UserCheckout, UserAddress

admin.site.register(Order)
admin.site.register(UserCheckout)
admin.site.register(UserAddress)