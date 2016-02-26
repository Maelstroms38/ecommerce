# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0011_myproducts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Thumbnail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('height', models.CharField(max_length=20, null=True, blank=True)),
                ('width', models.CharField(max_length=20, null=True, blank=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='myproducts',
            options={'verbose_name': 'My Products', 'verbose_name_plural': 'My Products'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['title'], 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AlterModelOptions(
            name='productfeatured',
            options={'verbose_name': 'Featured Product', 'verbose_name_plural': 'Featured Products'},
        ),
        migrations.AlterModelOptions(
            name='productimage',
            options={'verbose_name': 'Product Images', 'verbose_name_plural': 'Product Images'},
        ),
        migrations.AlterField(
            model_name='product',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='thumbnail',
            name='product',
            field=models.ForeignKey(to='products.Product'),
        ),
        migrations.AddField(
            model_name='thumbnail',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
