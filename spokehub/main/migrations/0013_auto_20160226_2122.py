# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations


def open_profiles(apps, schema_editor):
    User = apps.get_model("auth", "User")
    for u in User.objects.all():
        p = u.profile
        p.privacy = "open"
        p.save()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_remove_reply_title'),
    ]

    operations = [
        migrations.RunPython(open_profiles),
    ]
