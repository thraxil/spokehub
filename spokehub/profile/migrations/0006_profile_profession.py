# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0005_auto_20160227_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profession',
            field=models.CharField(default=b'', max_length=256, blank=True),
        ),
    ]
