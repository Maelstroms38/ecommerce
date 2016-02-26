# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20160119_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(default=0.99, max_digits=1000, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='variation',
            name='price',
            field=models.DecimalField(default=0.99, max_digits=20, decimal_places=2),
        ),
    ]
