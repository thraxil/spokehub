# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def merge_to_location(apps, schema_editor):
    User = apps.get_model("auth", "User")
    for u in User.objects.all():
        try:
            u.profile.location = "%s, %s" % (u.profile.city, u.profile.country)
            u.profile.save()
        except:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0003_profile_location'),
    ]

    operations = [
        migrations.RunPython(merge_to_location),
    ]
