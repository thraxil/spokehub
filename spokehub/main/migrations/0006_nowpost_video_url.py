# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20150322_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='nowpost',
            name='video_url',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
    ]
