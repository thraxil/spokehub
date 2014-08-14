from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from sorl.thumbnail.fields import ImageWithThumbnailsField
from south.modelsinspector import add_introspection_rules

import os.path
from django.template.defaultfilters import slugify


add_introspection_rules(
    [],
    ["sorl.thumbnail.fields.ImageWithThumbnailsField"])


class Item(models.Model):
    title = models.CharField(max_length=256)
    body = models.TextField(blank=True, default=u"")
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-added', ]

    def get_absolute_url(self):
        return "/item/%04d/%02d/%02d/%d/" % (
            self.added.year, self.added.month,
            self.added.day, self.id)

    def touch(self):
        self.modified = datetime.now()
        self.save()

    def add_reply(self, author, body):
        if not author:
            return
        if body.strip() == '':
            return
        Reply.objects.create(
            item=self,
            author=author,
            body=body)
        self.touch()


class Reply(models.Model):
    item = models.ForeignKey(Item)
    author = models.ForeignKey(User)
    body = models.TextField(blank=True, default=u"")
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        order_with_respect_to = 'item'
        ordering = ['added']


class WorkSample(models.Model):
    user = models.ForeignKey(User)
    image = ImageWithThumbnailsField(
        upload_to="images/%Y/%m/%d",
        thumbnail={
            'size': (400, 200)
            },
        )
    title = models.TextField(default="", blank=True)
    caption = models.TextField(default="", blank=True)

    def save_image(self, f):
        ext = f.name.split(".")[-1].lower()
        basename = slugify(f.name.split(".")[-2].lower())[:20]
        if ext not in ['jpg', 'jpeg', 'gif', 'png']:
            # unsupported image format
            return None
        now = datetime.now()
        path = "images/%04d/%02d/%02d/" % (now.year, now.month, now.day)
        try:
            os.makedirs(settings.MEDIA_ROOT + "/" + path)
        except:
            pass
        full_filename = path + "%s.%s" % (basename, ext)
        fd = open(settings.MEDIA_ROOT + "/" + full_filename, 'wb')
        for chunk in f.chunks():
            fd.write(chunk)
        fd.close()
        self.image = full_filename
        self.save()
