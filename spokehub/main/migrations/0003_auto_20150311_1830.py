# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150311_1746'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Item',
            new_name='Conversation',
        ),
    ]
