# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0007_auto_20160127_1605'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={},
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_total_price',
            field=models.DecimalField(default=5.99, max_digits=50, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(to='billing.UserCheckout', null=True),
        ),
    ]
