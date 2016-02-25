# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_nowpost_video_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reply',
            options={},
        ),
        migrations.AddField(
            model_name='conversation',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
