# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0033_auto_20160208_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='media',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location=b'/media/'), null=True, upload_to=products.models.download_media_location, blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='seller',
            field=models.ForeignKey(to='answers.AnswerAccount', null=True),
        ),
    ]
