from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.

class ProductQuerySet(models.QuerySet):
	def active(self):
		return self.filter(active=True)

class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model, using=self._db)

	def all(self, *args, **kwargs):
		return self.get_queryset().active()

class Product(models.Model):
	title = models.CharField(max_length=120)
	description = models.TextField(blank=True, null=True)
	price = models.DecimalField(decimal_places=2, max_digits=1000)
	active = models.BooleanField(default=True)
	#decription
	#active, answered
	#slug
	objects = ProductManager()

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("product_detail", kwargs={"pk": self.pk})

# Images, Categories

class Topic(models.Model):
    """
    Represents a high level topic.
    """
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return unicode(self.name)

class Concept(models.Model):
    """
    Represents a concept, which exists within a Topic
    """
    name = models.CharField(max_length=50)
    topic = models.ForeignKey(Topic)

    def __unicode__(self):
        return unicode(self.name)


class Example(models.Model):
    """
    Represents an example.  The fundamental data type for the application.
    """
    title     = models.CharField(max_length=50)
    content   = models.TextField()
    topic     = models.ForeignKey(Topic)
    concept   = models.ForeignKey(Concept)
    email     = models.CharField(max_length=100)
    link      = models.CharField(max_length=200, null=True)
    date      = models.DateField()
    picture   = models.ImageField(null=True)

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        ordering = ('title',)

class Answer(models.Model):
    """
    Represents a solution to an example.
    """
    example = models.ForeignKey(Example)
    content = models.TextField()

    def __unicode__(self):
        return unicode(self.example)
