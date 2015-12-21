from django.contrib import admin

# Register your models here.

from .models import Product, Example, Topic, Concept, Answer, Variation, ProductImage, Category

admin.site.register(Product)
admin.site.register(Example)
admin.site.register(Topic)
admin.site.register(Concept)
admin.site.register(Answer)
admin.site.register(Variation)
admin.site.register(ProductImage)
admin.site.register(Category)
