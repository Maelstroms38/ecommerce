from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.core.files.storage import FileSystemStorage
from answers.models import AnswerAccount
import os
import shutil
from PIL import Image
import random
from django.core.files import File
# Create your models here.

class ProductQuerySet(models.QuerySet):
	def active(self):
		return self.filter(active=True)

class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model, using=self._db)

	def all(self, *args, **kwargs):
		return self.get_queryset().active()
       
        def get_related(self, instance):
            products_one = self.get_queryset().filter(categories__in = instance.categories.all())
            products_two = self.get_queryset().filter(default=instance.default)
            qs = (products_one | products_two).exclude(id=instance.id).distinct
            return qs #self.get_queryset()

def download_media_location(instance, filename):
    return "media/%s/%s" %(instance.slug, filename)

class Product(models.Model):
	title = models.CharField(max_length=120)
	description = models.TextField(blank=True, null=True)
	price = models.DecimalField(decimal_places=2, max_digits=1000, default=0.99)
	active = models.BooleanField(default=True)
        slug = models.SlugField(blank=True, unique=True)
        embed_code = models.CharField(max_length=500, null=True, blank=True)
        seller = models.ForeignKey(AnswerAccount, null=True, blank=True)
        media = models.FileField(blank=True, null=True, upload_to=download_media_location, storage=FileSystemStorage(location=settings.MEDIA_URL))
        categories = models.ManyToManyField('Category', blank=True)
        default = models.ForeignKey('Category', related_name='default_category', null=True, blank=True)
    
	objects = ProductManager()

        class Meta:
            ordering = ["title"]
            verbose_name = "Product"
            verbose_name_plural = "Products"

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("product_detail", kwargs={"pk": self.pk})
        def get_image_url(self):
            img = self.productimage_set.first()
            if img:
                return img.image.url
            return img #none
        def get_download(self):
           url = reverse("download_slug", kwargs={"slug": self.slug})
           return url

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug

    qs = Product.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id) 
        return create_slug(instance, new_slug=new_slug)
    return slug

def product_pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(product_pre_save_reciever, sender=Product)

def thumbnail_location(instance, filename):
    return "thumbnails/%s/%s" %(instance.product.slug, filename)
THUMB_CHOICES = (
    ("hd", "HD"),
    ("sd", "SD"),
    ("micro", "Micro"),
)

class Thumbnail(models.Model):
    product = models.ForeignKey(Product)
    type = models.CharField(max_length=20, choices=THUMB_CHOICES, default='hd')
    height = models.CharField(max_length=20, null=True, blank=True) 
    width = models.CharField(max_length=20, null=True, blank=True)
    media = models.ImageField(width_field= "width", height_field="height", blank=True, null=True, upload_to=thumbnail_location)

    def __unicode__(self):
        return str(self.media)

def create_new_thumb(media_path, instance, owner_slug, max_length, max_width):
    filename = os.path.basename(media_path)
    thumb = Image.open(media_path)
    size = (max_length, max_width)
    thumb.thumbnail(size, Image.ANTIALIAS)
    temp_loc = "%s/%s/tmp" %(settings.MEDIA_URL, owner_slug)
    if not os.path.exists(temp_loc):
        os.makedirs(temp_loc)
    temp_file_path = os.path.join(temp_loc, filename)
    if os.path.exists(temp_file_path):
        temp_path = os.path.join(temp_loc, "%s" %(random.random()))
        os.makedirs(temp_path)
        temp_file_path = os.path.join(temp_path, filename)

    temp_image = open(temp_file_path, "w")
    thumb.save(temp_image)
    thumb_data = open(temp_file_path, "r")

    thumb_file = File(thumb_data)
    instance.media.save(filename, thumb_file)
    shutil.rmtree(temp_loc, ignore_errors=True)
    return True

def product_post_save_reciever(sender, instance, created, *args, **kwargs):
    hd, hd_created = Thumbnail.objects.get_or_create(product=instance, type='hd')
    # sd, sd_created = Thumbnail.objects.get_or_create(product=instance, type='sd')
    # micro, micro_created = Thumbnail.objects.get_or_create(product=instance, type='micro')

    hd_max = (500, 500)
    sd_max = (350, 350)
    micro_max = (150, 150)

    if instance.media:
        media_path = instance.media.path
        owner_slug = instance.slug
        if hd_created:
            create_new_thumb(media_path, hd, owner_slug, hd_max[0], hd_max[1])
    
    # if sd_created:
    #     create_new_thumb(media_path, sd, owner_slug, sd_max[0], sd_max[1])

    # if micro_created:
    #     create_new_thumb(media_path, micro, owner_slug, micro_max[0], micro_max[1])

post_save.connect(product_post_save_reciever, sender=Product)

class MyProducts(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    products = models.ManyToManyField(Product, blank=True)

    def __unicode__(self):
        return "%s" %(self.products.count())
    class Meta:
        verbose_name = "My Products"
        verbose_name_plural = "My Products"


class Variation(models.Model):
    product = models.ForeignKey(Product)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    inventory = models.IntegerField(null=True, blank=True) #unlimited amount
    price = models.DecimalField(decimal_places=2, max_digits=20, default=0.99)
    sale_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

    def get_html_price(self):
        if self.sale_price is not None:
            html_text = "<span class='sale-price'>%s</span> <span class='og-price'>%s</span>" %(self.sale_price, self.price)
        else:
            html_text = "<span class='price'>%s</span>" %(self.price)
        return mark_safe(html_text)

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def add_to_cart(self):
        return "%s?item=%s&qty=1" %(reverse("cart"), self.id)

    def remove_from_cart(self):
        return "%s?item=%s&qty=1&delete=True" %(reverse("cart"), self.id)

    def get_title(self):
        return "%s - %s" %(self.product.title, self.title)

def product_post_saved_reciever(sender, instance, created, *args, **kwargs):
    product = instance
    variations = product.variation_set.all()
    if variations.count() == 0:
        new_var = Variation()
        new_var.product = product
        new_var.title = "Default"
        new_var.price = product.price
        new_var.save()

post_save.connect(product_post_saved_reciever, sender=Product)

def image_upload_to(instance, filename):
    title = instance.product.title
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    qs = Product.objects.filter(slug=slug)
    exists = qs.exists()
    if qs:
        new_filename = "%s-%s.%s" %(slug, qs.first().id, file_extension)
    return "products/%s/%s" %(slug, new_filename)

class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to=image_upload_to)

    def __unicode__(self):
        return self.product.title

    class Meta:
        verbose_name = "Product Images"
        verbose_name_plural = "Product Images"

def image_upload_to_featured(instance, filename):
    title = instance.product.title
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    qs = Product.objects.filter(slug=slug)
    exists = qs.exists()
    if qs:
        new_filename = "%s-%s.%s" %(slug, qs.first().id, file_extension)
    return "products/%s/featured/%s" %(slug, new_filename)

class ProductFeatured(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to=image_upload_to_featured)
    title = models.CharField(max_length=120, null=True, blank=True)
    text = models.CharField(max_length=220, null=True, blank=True)
    text_right = models.BooleanField(default=False)
    show_price = models.BooleanField(default=False)
    make_image_background = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Featured Product"
        verbose_name_plural = "Featured Products"

    def __unicode__(self):
        return self.product.title

# Images, Categories
class Category(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug })
