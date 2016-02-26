# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_product_embed_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='managers',
        ),
        migrations.AlterField(
            model_name='product',
            name='user',
            field=models.ForeignKey(to='answers.AnswerAccount'),
        ),
    ]
