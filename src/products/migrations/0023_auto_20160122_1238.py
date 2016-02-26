# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_auto_20160122_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='media',
            field=models.FileField(default=1, storage=django.core.files.storage.FileSystemStorage(location=b'/Users/michaelstromer/Documents/Codes/Portfolio/Django/ecommerce/static_in_env/protected_root'), upload_to=products.models.download_media_location, blank=True),
            preserve_default=False,
        ),
    ]
