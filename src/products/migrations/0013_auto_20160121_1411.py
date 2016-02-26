# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20160121_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='user',
            field=models.ForeignKey(default=1, blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
