# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='twitteraccount',
            name='user',
        ),
        migrations.DeleteModel(
            name='TwitterAccount',
        ),
    ]
