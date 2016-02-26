# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0027_variation_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='media',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location=b'/Users/michaelstromer/Documents/Codes/Portfolio/Django/ecommerce/static/protected_root'), null=True, upload_to=products.models.download_media_location, blank=True),
        ),
    ]
