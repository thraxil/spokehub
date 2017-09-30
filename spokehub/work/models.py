import os.path
import urllib.parse as urlparse

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    title = models.TextField(blank=True, default="")
    slug = models.SlugField(
        help_text="""The slug is the bit that goes in the URL. """
        """So, <tt>https://spokehub.org/work/<b>this-is-the-slug</b>/</tt>. """
        """Keep it short, lowercase, no spaces or punctuation other """
        """than dashes, and slugs must all be unique.""")
    subhead = models.TextField(blank=True, default="")
    date = models.TextField(blank=True, default="")
    description = models.TextField(
        blank=True, default="",
        help_text="""<a href="https://github.com/adam-p/"""
        """markdown-here/wiki/Markdown-Cheatsheet">Markdown</a> """
        """and simple HTML may be used here.""")
    published = models.BooleanField(default=False)
    thumb_hash = models.TextField(blank=True, null=True)
    thumb_extension = models.TextField(blank=True, null=True)
    cardinality = models.IntegerField(default=1)

    class Meta:
        ordering = ['-cardinality']

    def save_thumbnail(self, f):
        ext = os.path.splitext(f.name)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.gif', '.png']:
            # unsupported image format
            return None
        self.thumb_hash = settings.UPLOADER.upload(f)
        self.thumb_extension = ext
        self.save()

    def add_image(self, f):
        ext = os.path.splitext(f.name)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.gif', '.png']:
            # unsupported image format
            return None
        rhash = settings.UPLOADER.upload(f)
        self.projectmedia_set.create(
            image_hash=rhash,
            image_extension=ext,
        )

    def publish(self):
        self.published = True
        self.save()

    def draft(self):
        self.published = False
        self.save()

    def add_youtube(self, url):
        if 'youtube.com' in url:
            url_data = urlparse.urlparse(url)
            query = urlparse.parse_qs(url_data.query)
            youtube_id = query["v"][0]
            self.projectmedia_set.create(youtube_id=youtube_id)

    def add_vimeo(self, url):
        if 'vimeo.com' in url:
            url_data = urlparse.urlparse(url)
            vimeo_id = url_data.path[1:]
            self.projectmedia_set.create(vimeo_id=vimeo_id)

    def next(self):
        next = Project.objects.filter(
            cardinality__lt=self.cardinality,
            published=True).first()
        if next:
            return next
        else:
            return Project.objects.filter(
                published=True).order_by("-cardinality").first()

    def previous(self):
        previous = Project.objects.filter(
            cardinality__gt=self.cardinality,
            published=True).first()
        if previous:
            return previous
        else:
            return Project.objects.filter(
                published=True).order_by("cardinality").first()


class ProjectContributor(models.Model):
    project = models.ForeignKey(Project)
    fullname = models.TextField(blank=True, default="")
    user = models.ForeignKey(User, null=True)

    class Meta:
        order_with_respect_to = 'project'


class ProjectMedia(models.Model):
    project = models.ForeignKey(Project)
    image_hash = models.TextField(blank=True, null=True)
    image_extension = models.TextField(blank=True, null=True)
    youtube_id = models.TextField(default="", blank=True)
    vimeo_id = models.TextField(default="", blank=True)

    class Meta:
        order_with_respect_to = 'project'
