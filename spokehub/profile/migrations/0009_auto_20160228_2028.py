# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def force_open(apps, schema_editor):
    User = apps.get_model("auth", "user")
    for u in User.objects.all():
        try:
            u.profile.privacy = "open"
            u.save()
        except:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0008_profile_cover'),
    ]

    operations = [
        migrations.RunPython(force_open),
    ]
