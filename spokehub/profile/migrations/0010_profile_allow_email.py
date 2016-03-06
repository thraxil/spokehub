# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0009_auto_20160228_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='allow_email',
            field=models.BooleanField(default=False),
        ),
    ]
