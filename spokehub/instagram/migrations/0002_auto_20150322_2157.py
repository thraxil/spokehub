# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instagramaccount',
            name='user',
        ),
        migrations.DeleteModel(
            name='InstagramAccount',
        ),
    ]
