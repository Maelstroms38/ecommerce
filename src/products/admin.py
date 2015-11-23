from django.contrib import admin

# Register your models here.

from .models import Product, Example, Topic, Concept, Answer

admin.site.register(Product)
admin.site.register(Example)
admin.site.register(Topic)
admin.site.register(Concept)
admin.site.register(Answer)
