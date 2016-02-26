# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0006_auto_20160124_1107'),
        ('billing', '0004_useraddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shipping_price', models.DecimalField(default=5.99, max_digits=50, decimal_places=2)),
                ('order_total', models.DecimalField(max_digits=50, decimal_places=2)),
                ('billing_address', models.ForeignKey(related_name='billing_address', to='billing.UserCheckout')),
                ('cart', models.ForeignKey(to='carts.Cart')),
                ('shipping_address', models.ForeignKey(related_name='shipping_address', to='billing.UserCheckout')),
                ('user', models.ForeignKey(to='billing.UserCheckout')),
            ],
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='product',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='user',
        ),
        migrations.DeleteModel(
            name='Transaction',
        ),
    ]
