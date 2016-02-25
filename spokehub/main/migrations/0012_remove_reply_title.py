# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_remove_conversation_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reply',
            name='title',
        ),
    ]
