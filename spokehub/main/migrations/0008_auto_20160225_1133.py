# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def assign_authors(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    User = apps.get_model("auth", "User")
    Conversation = apps.get_model("main", "Conversation")

    default_user = User.objects.filter(is_superuser=True).first()
    try:
        # in production, just make onika the default
        default_user = User.objects.get(username='onika')
    except User.DoesNotExist:
        pass

    for c in Conversation.objects.filter(author=None):
        c.author = default_user
        c.save()
        print("assigned %d author %s" % (c.id, default_user.username))


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20160225_1130'),
    ]

    operations = [
        migrations.RunPython(assign_authors),
    ]
