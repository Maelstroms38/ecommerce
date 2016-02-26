# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_auto_20160122_1034'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='user',
            new_name='seller',
        ),
    ]
