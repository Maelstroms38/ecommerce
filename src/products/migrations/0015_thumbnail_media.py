# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_auto_20160121_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='thumbnail',
            name='media',
            field=models.ImageField(height_field=b'height', width_field=b'width', null=True, upload_to=products.models.download_media_location, blank=True),
        ),
    ]
