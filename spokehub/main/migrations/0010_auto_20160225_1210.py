# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20160225_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE),
        ),
    ]
