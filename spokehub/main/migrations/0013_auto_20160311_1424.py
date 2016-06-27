# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_remove_reply_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='image',
            field=models.TextField(null=True, blank=True),
        ),
    ]
