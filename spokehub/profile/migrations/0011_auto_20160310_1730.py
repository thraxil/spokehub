# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0010_profile_allow_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profession',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='profile',
            name='website_name',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='profile',
            name='website_url',
            field=models.CharField(max_length=256),
        ),
    ]
