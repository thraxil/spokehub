# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('body', models.TextField(default='', blank=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('image', sorl.thumbnail.fields.ImageWithThumbnailsField(null=True, upload_to=b'convoimages/%Y/%m/%d')),
            ],
            options={
                'ordering': ['-added'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NowPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField()),
                ('service', models.TextField(default=b'', blank=True)),
                ('service_id', models.TextField(default=b'', blank=True)),
                ('text', models.TextField(default=b'', blank=True)),
                ('original', models.TextField(default=b'', blank=True)),
                ('image_url', models.TextField(default=b'', blank=True)),
                ('image_width', models.IntegerField(default=0)),
                ('image_height', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField(default='', blank=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('image', sorl.thumbnail.fields.ImageWithThumbnailsField(null=True, upload_to=b'replyimages/%Y/%m/%d')),
                ('url', models.TextField(default='', blank=True)),
                ('title', models.TextField(default='', blank=True)),
                ('youtube_id', models.TextField(default=b'', blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(to='main.Item')),
            ],
            options={
                'ordering': ['added'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkSample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', sorl.thumbnail.fields.ImageWithThumbnailsField(upload_to=b'images/%Y/%m/%d')),
                ('title', models.TextField(default=b'', blank=True)),
                ('youtube_id', models.TextField(default=b'', blank=True)),
                ('vimeo_id', models.TextField(default=b'', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterOrderWithRespectTo(
            name='reply',
            order_with_respect_to='item',
        ),
    ]
