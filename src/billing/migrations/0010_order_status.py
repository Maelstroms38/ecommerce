# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0009_auto_20160128_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default=b'created', max_length=120, choices=[(b'created', b'Created'), (b'completed', b'Completed')]),
        ),
    ]
