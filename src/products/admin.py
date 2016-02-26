from django.contrib import admin

# Register your models here.

from .models import Product, Variation, ProductImage, Thumbnail, Category, ProductFeatured, MyProducts

class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 0

class VariationInline(admin.TabularInline):
	model = Variation
	extra = 0

class ProductAdmin(admin.ModelAdmin):
	list_display = ['__unicode__', 'price']
	inlines = [
		VariationInline,
		ProductImageInline,
	]
	class Meta:
		model = Product
class ThumbnailInline(admin.TabularInline):
	extra = 1
	model = Thumbnail


# class ProductAdmin(admin.ModelAdmin):
# 	inlines = [ThumbnailInline]
# 	list_display = ["__unicode__", "description", "price", "media"]
# 	search_fields = ["title", "description"]
# 	#fields = ["title", "description", "embed_code", "slug"]
# 	list_filter = ["price"]
# 	#list_editable = ["sale_price"]
# 	class Meta:
# 		model = Product

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(ProductFeatured)
admin.site.register(MyProducts)
admin.site.register(Thumbnail)
admin.site.register(Variation)