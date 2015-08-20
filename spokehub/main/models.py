from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from sorl.thumbnail.fields import ImageWithThumbnailsField
import re
import os.path
from django.template.defaultfilters import slugify
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
import urlparse


class Conversation(models.Model):
    title = models.CharField(max_length=256)
    body = models.TextField(blank=True, default=u"")
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    image = ImageWithThumbnailsField(
        upload_to="convoimages/%Y/%m/%d",
        thumbnail={
            'size': (400, 200)
            },
        null=True,
        )

    class Meta:
        ordering = ['-added', ]

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'conversation', args=[
                "%04d" % self.added.year,
                "%02d" % self.added.month,
                "%02d" % self.added.day,
                str(self.id)])

    def touch(self):
        self.modified = datetime.now()
        self.save()

    def add_reply(self, author, body, url='', title=''):
        if not author:
            return
        if body.strip() == '' and url.strip() == '':
            return
        if (url.strip() != '' and
                not (url.startswith('http://') or url.startswith('https://'))):
            url = "http://" + url
        r = Reply.objects.create(
            item=self,
            author=author,
            body=body,
            url=url.strip(), title=title.strip())
        if 'youtube.com' in url:
            url_data = urlparse.urlparse(r.url)
            query = urlparse.parse_qs(url_data.query)
            r.youtube_id = query["v"][0]
            r.save()
        if 'vimeo.com' in url:
            url_data = urlparse.urlparse(r.url)
            r.vimeo_id = url_data.path[1:]
            r.save()
        self.touch()
        return r


@receiver(post_save, sender=Conversation)
def new_conversation_emails(sender, **kwargs):
    if not kwargs.get('created', False):
        # only send it on creation
        return
    for u in User.objects.all():
        if u.is_anonymous() or u.username == 'AnonymousUser':
            continue
        i = kwargs['instance']
        u.email_user(
            "[spokehub] new conversation: " + i.title,
            i.body + "\n\n---\nhttp://spokehub.org/\n",
            'hello@spokehub.org')


class Reply(models.Model):
    item = models.ForeignKey(Conversation)
    author = models.ForeignKey(User)
    body = models.TextField(blank=True, default=u"")
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    image = ImageWithThumbnailsField(
        upload_to="replyimages/%Y/%m/%d",
        thumbnail={
            'size': (400, 200)
            },
        null=True,
        )
    url = models.TextField(blank=True, default=u"")
    title = models.TextField(blank=True, default=u"")
    youtube_id = models.TextField(default="", blank=True)
    vimeo_id = models.TextField(default="", blank=True)

    class Meta:
        order_with_respect_to = 'item'
        ordering = ['added']

    def __unicode__(self):
        return "Reply to [%s] by %s at %s" % (
            str(self.item),
            self.author.username,
            self.added.isoformat())

    def save_image(self, f):
        ext = f.name.split(".")[-1].lower()
        basename = slugify(f.name.split(".")[-2].lower())[:20]
        if ext not in ['jpg', 'jpeg', 'gif', 'png']:
            # unsupported image format
            return None
        now = datetime.now()
        path = "replyimages/%04d/%02d/%02d/" % (now.year, now.month, now.day)
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

    def mentioned_users(self):
        pattern = re.compile('\@(\w+)', re.MULTILINE)
        usernames = [u.lower() for u in pattern.findall(self.body)]
        usernames = list(set(usernames))
        users = []
        for u in usernames:
            if u == self.author.username:
                continue
            r = User.objects.filter(username__iexact=u)
            if not r.exists():
                continue
            users.append(r[0])
        return users

    def conversation_users(self):
        users = []
        for r in self.item.reply_set.all():
            if r.author.username == self.author.username:
                continue
            users.append(r.author)
        return list(set(users))

    def all_mentioned_users(self):
        pattern = re.compile('\@(\w+)', re.MULTILINE)
        usernames = [u.lower() for u in pattern.findall(self.body)]
        usernames = list(set(usernames))
        users = []
        for u in usernames:
            r = User.objects.filter(username__iexact=u)
            if not r.exists():
                continue
            users.append(r[0])
        return users

    def link_usernames(self):
        body = self.body
        for u in self.all_mentioned_users():
            link = reverse('userena_profile_detail', args=[u.username, ])
            body = re.sub(
                '@' + u.username,
                '[@%s](%s)' % (u.username, link),
                body
            )
        return body

    def email_mentions(self):
        conv_users = self.conversation_users()
        mentioned = self.mentioned_users()
        unmentioned = set(conv_users) - set(mentioned)
        for user in mentioned:
            user.email_user(
                "[spokehub] someone mentioned you on spokehub",
                """%s mentioned you in a reply:

%s
""" % (self.author.username, self.body),
                'hello@spokehub.org',
                )
        for user in unmentioned:
            user.email_user(
                "[spokehub] conversation reply",
                """%s replied to a spokehub conversation that you
are participating in:

%s
""" % (self.author.username, self.body))

    def is_video(self):
        if self.url == "":
            return False
        return 'youtube.com' in self.url or 'vimeo.com' in self.url

    def is_youtube(self):
        return self.youtube_id != ""

    def is_vimeo(self):
        return self.vimeo_id != ""


class NowPost(models.Model):
    screen_name = models.TextField(default="", blank=True)
    created = models.DateTimeField()
    service = models.TextField(default="", blank=True)
    service_id = models.TextField(default="", blank=True)
    text = models.TextField(default="", blank=True)
    original = models.TextField(default="", blank=True)

    image_url = models.TextField(default="", blank=True)
    image_width = models.IntegerField(default=0)
    image_height = models.IntegerField(default=0)

    video_url = models.TextField(default="", blank=True)

    def __unicode__(self):
        return "[%s] by %s at %s" % (self.service, self.screen_name,
                                     self.created.isoformat())

    def external_link(self):
        # expand for other services later
        if self.service == 'twitter':
            return ("https://twitter.com/%s/status/%s" % (
                self.screen_name, self.service_id))
        elif self.service == 'instagram':
            return self.service_id
        elif self.service == 'tumblr':
            return self.service_id
        else:
            return None
