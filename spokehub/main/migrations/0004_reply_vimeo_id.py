# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20150311_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='vimeo_id',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
    ]
