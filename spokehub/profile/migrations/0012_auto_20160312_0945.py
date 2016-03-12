# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0011_auto_20160310_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='allow_email',
            field=models.BooleanField(default=False, verbose_name=b'Allow Notifications'),
        ),
    ]
