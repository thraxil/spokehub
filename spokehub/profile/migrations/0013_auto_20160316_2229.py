# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0012_auto_20160312_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cover',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'covers', verbose_name=b'Your background image', blank=True),
        ),
    ]
