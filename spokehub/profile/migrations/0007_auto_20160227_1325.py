# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0006_profile_profession'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='discipline1',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='discipline2',
        ),
    ]
