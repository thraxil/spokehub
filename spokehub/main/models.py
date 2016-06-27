from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from sorl.thumbnail.fields import ImageWithThumbnailsField
import re
import os.path
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.template import Context
from userena.utils import get_user_profile
import urlparse
import waffle


class ConversationManager(models.Manager):
    def newest(self):
        return Conversation.objects.all().order_by('-added')[:10]


class Conversation(models.Model):
    body = models.TextField(blank=True, default=u"")
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    image = ImageWithThumbnailsField(
        upload_to="convoimages/%Y/%m/%d",
        thumbnail={
            'size': (400, 200)
            },
        null=True,
        blank=True,
        )
    author = models.ForeignKey(User)
    rhash = models.TextField(blank=True, null=True)

    objects = ConversationManager()

    class Meta:
        ordering = ['-added', ]

    def __unicode__(self):
        return self.body[:140]

    def url_args(self):
        return [
            "%04d" % self.added.year,
            "%02d" % self.added.month,
            "%02d" % self.added.day,
            str(self.id)]

    def get_absolute_url(self):
        return reverse('question', args=self.url_args())

    def get_edit_url(self):
        return reverse('edit-question', args=self.url_args())

    def get_delete_url(self):
        return reverse('delete-question', args=self.url_args())

    def touch(self):
        self.modified = datetime.now()
        self.save()

    def add_reply(self, author, body, url='', image=None):
        if not author:
            return
        if body.strip() == '' and url.strip() == '' and image is None:
            return
        if (url.strip() != '' and
                not (url.startswith('http://') or url.startswith('https://'))):
            url = "http://" + url
        r = Reply.objects.create_reply(self, author, body, url)
        r.save()
        self.touch()
        if image is not None:
            r.save_image(image)
        r.email_mentions()
        r.body = r.link_usernames()
        r.save()
        return r


@receiver(post_save, sender=Conversation)
def new_conversation_emails(sender, **kwargs):
    if not kwargs.get('created', False):
        # only send it on creation
        return
    if settings.DEBUG:
        # don't do this in dev/staging
        return
    i = kwargs['instance']
    for u in User.objects.all():
        user_new_convo_email(u, i)


def user_new_convo_email(u, i):
    profile = get_user_profile(u)
    if (u.is_anonymous() or u.username == 'AnonymousUser' or
            not profile.allow_email):
        return
    if waffle.switch_is_active('send_email') or u.is_staff:
        plaintext = get_template('email/new_question.txt')
        htmltext = get_template('email/new_question.html')
        d = Context({'question': i})
        text_content = plaintext.render(d)
        html_content = htmltext.render(d)
        u.email_user(
            "[spokehub] new conversation: ",
            text_content,
            'Hub Conversation <hello@spokehub.org>',
            html_message=html_content,
        )


class ReplyManager(models.Manager):
    def create_reply(self, item, author, body, url):
        r = Reply(
            item=item,
            author=author,
            body=body,
            url=url.strip())
        r.set_video_ids()
        r.save()
        return r


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
        blank=True,
        )
    url = models.TextField(blank=True, default=u"")
    youtube_id = models.TextField(default="", blank=True)
    vimeo_id = models.TextField(default="", blank=True)
    rhash = models.TextField(blank=True, null=True)

    objects = ReplyManager()

    class Meta:
        order_with_respect_to = 'item'

    def __unicode__(self):
        return "Reply to [%s] by %s at %s" % (
            str(self.item),
            self.author.username,
            self.added.isoformat())

    def set_video_ids(self):
        if 'youtube.com' in self.url:
            url_data = urlparse.urlparse(self.url)
            query = urlparse.parse_qs(url_data.query)
            self.youtube_id = query["v"][0]
        if 'vimeo.com' in self.url:
            url_data = urlparse.urlparse(self.url)
            self.vimeo_id = url_data.path[1:]

    def save_image(self, f):
        ext = os.path.splitext(f.name)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.gif', '.png']:
            # unsupported image format
            return None
        self.rhash = settings.UPLOADER.upload(f)
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
        if settings.DEBUG:
            # don't do this in dev/staging
            return
        conv_users = self.conversation_users()
        mentioned = self.mentioned_users()
        unmentioned = set(conv_users) - set(mentioned)
        d = Context({'reply': self})

        self.email_mentioned(mentioned, d)
        self.email_unmentioned(unmentioned, d)

    def email_mentioned(self, mentioned, d):
        for user in mentioned:
            if not get_user_profile(user).allow_email:
                continue
            plaintext = get_template('email/mentioned.txt')
            htmltext = get_template('email/mentioned.html')
            text_content = plaintext.render(d)
            html_content = htmltext.render(d)
            user.email_user(
                "[spokehub] someone mentioned you on spokehub",
                text_content,
                'Hub Conversation <hello@spokehub.org>',
                html_message=html_content,
                )

    def email_unmentioned(self, unmentioned, d):
        for user in unmentioned:
            if not get_user_profile(user).allow_email:
                continue
            plaintext = get_template('email/reply.txt')
            htmltext = get_template('email/reply.html')
            text_content = plaintext.render(d)
            html_content = htmltext.render(d)
            user.email_user(
                "[spokehub] conversation reply",
                text_content,
                'Hub Conversation <hello@spokehub.org>',
                html_message=html_content,
            )

    def is_video(self):
        if self.url == "":
            return False
        return 'youtube.com' in self.url or 'vimeo.com' in self.url

    def get_youtube_id(self):
        if 'youtube.com' in self.url:
            url_data = urlparse.urlparse(self.url)
            query = urlparse.parse_qs(url_data.query)
            return query["v"][0]
        return ""

    def is_youtube(self):
        return self.get_youtube_id() != ""

    def get_vimeo_id(self):
        if 'vimeo.com' in self.url:
            url_data = urlparse.urlparse(self.url)
            return url_data.path[1:]
        return ""

    def is_vimeo(self):
        return self.get_vimeo_id() != ""

    def add_comment(self, author, body):
        return Comment.objects.create(
            self, author, body)


class CommentManager(models.Manager):
    def create(self, reply, author, body):
        c = Comment(
            reply=reply,
            author=author,
            body=body,
        )
        c.save()
        return c


class Comment(models.Model):
    reply = models.ForeignKey(Reply)
    added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    body = models.TextField(blank=True, default=u"")

    objects = CommentManager()

    class Meta:
        ordering = ["added"]


class NowPostManager(models.Manager):
    def newest(self):
        return NowPost.objects.all().order_by("-created")

    def create_instagram(self, screen_name, service_id, text, created,
                         image_url, video_url, original_json):
        np = NowPost(
            screen_name=screen_name,
            service='instagram',
            service_id=service_id,
            text=text,
            created=created,
            image_url=image_url,
            video_url=video_url,
            image_width=640,
            image_height=640,
            original=original_json,
        )
        np.save()
        return np

    def create_twitter(self, screen_name, service_id, text, created,
                       original_json):
        np = NowPost(
            screen_name=screen_name,
            service='twitter',
            service_id=service_id,
            text=text,
            created=created,
            original=original_json,
            )
        np.save()
        return np

    def create_tumblr(self, screen_name, service_id, text, created, image_url,
                      image_width, image_height, original_json):
        np = NowPost(
            screen_name=screen_name,
            service='tumblr',
            service_id=service_id,
            text=text,
            created=created,
            image_url=image_url,
            video_url="",
            image_width=image_width,
            image_height=image_height,
            original=original_json,
        )
        np.save()
        return np


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

    objects = NowPostManager()

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
