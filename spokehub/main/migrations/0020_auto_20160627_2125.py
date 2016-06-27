# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-27 21:25
from __future__ import unicode_literals

from django.db import migrations
import os.path
import requests
from django.conf import settings


def upload_reply_images_to_reticulum(apps, schema_editor):
    Reply = apps.get_model("main", "Reply")
    for reply in Reply.objects.all():
        if reply.rhash or not reply.image:
            continue
        fullpath = os.path.join(settings.MEDIA_ROOT, str(reply.image))
        extension = os.path.splitext(fullpath)[1].lower()
        basename = os.path.basename(fullpath)
        try:
            with open(fullpath, 'rb') as f:
                files = {
                    'image': (basename, f),
                }
                r = requests.post(settings.RETICULUM_UPLOAD + "/", files=files,
                                  verify=False)
                reply.rhash = r.json()["hash"]
                reply.extension = extension
                reply.save()
                print("uploaded " + str(reply.image))
        except IOError:
            pass


def upload_convo_images_to_reticulum(apps, schema_editor):
    Conversation = apps.get_model("main", "Conversation")
    for conversation in Conversation.objects.all():
        if conversation.rhash or not conversation.image:
            continue
        fullpath = os.path.join(settings.MEDIA_ROOT, str(conversation.image))
        extension = os.path.splitext(fullpath)[1].lower()
        basename = os.path.basename(fullpath)
        try:
            with open(fullpath, 'rb') as f:
                files = {
                    'image': (basename, f),
                }
                r = requests.post(settings.RETICULUM_UPLOAD + "/", files=files,
                                  verify=False)
                conversation.rhash = r.json()["hash"]
                conversation.extension = extension
                conversation.save()
                print("uploaded " + str(conversation.image))
        except IOError:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20160627_2124'),
    ]

    operations = [
        migrations.RunPython(upload_convo_images_to_reticulum),
        migrations.RunPython(upload_reply_images_to_reticulum),
    ]
