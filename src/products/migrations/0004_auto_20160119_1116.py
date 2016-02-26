# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20160119_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='price',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=2),
        ),
    ]
