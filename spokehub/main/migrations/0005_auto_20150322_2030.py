# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_reply_vimeo_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nowpost',
            name='user',
        ),
        migrations.AddField(
            model_name='nowpost',
            name='screen_name',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
    ]
