# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_thumbnail_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thumbnail',
            name='user',
        ),
    ]
