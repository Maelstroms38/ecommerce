# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0026_auto_20160127_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
    ]
