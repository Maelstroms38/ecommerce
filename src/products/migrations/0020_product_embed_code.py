# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_remove_thumbnail_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='embed_code',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
    ]
