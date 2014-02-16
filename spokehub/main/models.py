from django.contrib.auth.models import User
from django.db import models


class Item(models.Model):
    title = models.CharField(max_length=256)
    section = models.CharField(
        max_length=256,
        choices=(('news', 'News Item'),
                 ('challenge', 'Challenge'),
                 ('case', 'Case Study')))
    body = models.TextField(blank=True, default=u"")
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User)

    class Meta:
        ordering = ['section', 'added']


class Reply(models.Model):
    item = models.ForeignKey(Item)
    author = models.ForeignKey(User)
    body = models.TextField(blank=True, default=u"")
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        order_with_respect_to = 'item'
        ordering = ['added']
