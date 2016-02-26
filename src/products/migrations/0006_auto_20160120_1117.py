# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20160119_1341'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='example',
        ),
        migrations.RemoveField(
            model_name='concept',
            name='topic',
        ),
        migrations.RemoveField(
            model_name='example',
            name='concept',
        ),
        migrations.RemoveField(
            model_name='example',
            name='topic',
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(unique=True, blank=True),
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.DeleteModel(
            name='Concept',
        ),
        migrations.DeleteModel(
            name='Example',
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
    ]
