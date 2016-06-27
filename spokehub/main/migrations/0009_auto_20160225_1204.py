# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20160225_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='image',
            field=models.TextField(null=True, blank=True),
        ),
    ]
