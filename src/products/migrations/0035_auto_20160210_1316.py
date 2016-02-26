# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0034_auto_20160210_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='media',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location=b'http://examplefy.s3.amazonaws.com/'), null=True, upload_to=products.models.download_media_location, blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='seller',
            field=models.ForeignKey(blank=True, to='answers.AnswerAccount', null=True),
        ),
    ]
