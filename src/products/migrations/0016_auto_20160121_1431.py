# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_thumbnail_media'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='user',
        ),
        migrations.AlterField(
            model_name='thumbnail',
            name='media',
            field=models.ImageField(height_field=b'height', width_field=b'width', null=True, upload_to=products.models.thumbnail_location, blank=True),
        ),
    ]
