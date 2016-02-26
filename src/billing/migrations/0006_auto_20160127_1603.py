# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0005_auto_20160127_1502'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterModelOptions(
            name='useraddress',
            options={'verbose_name': 'User Address', 'verbose_name_plural': 'User Addresses'},
        ),
        migrations.AlterModelOptions(
            name='usercheckout',
            options={'verbose_name': 'User Checkout', 'verbose_name_plural': 'User Checkouts'},
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_price',
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_total_price',
            field=models.DecimalField(default=1.99, max_digits=50, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='order',
            name='billing_address',
            field=models.ForeignKey(related_name='billing_address', to='billing.UserAddress'),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(related_name='shipping_address', to='billing.UserAddress'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='type',
            field=models.CharField(max_length=120, choices=[(b'billing', b'Billing'), (b'shipping', b'Shipping')]),
        ),
    ]
