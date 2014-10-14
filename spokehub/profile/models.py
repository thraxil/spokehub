from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile
from spokehub.main.models import WorkSample
from spokehub.twitter.models import TwitterAccount
from spokehub.instagram.models import InstagramAccount
from spokehub.feed.models import UserFeed


class Profile(UserenaBaseProfile):
    user = models.OneToOneField(
        User,
        unique=True,
        verbose_name=_('user'),
        related_name='profile')
    about_me = models.TextField(blank=True, default="")
    city = models.CharField(max_length=256, blank=True, default="")
    country = models.CharField(max_length=256, blank=True, default="")
    discipline1 = models.CharField(max_length=256, blank=True, default="")
    discipline2 = models.CharField(max_length=256, blank=True, default="")
    website_url = models.CharField(max_length=256, blank=True, default="")
    website_name = models.CharField(max_length=256, blank=True, default="")

    def work_samples(self):
        return WorkSample.objects.filter(user=self.user)

    def twitter(self):
        r = TwitterAccount.objects.filter(user=self)
        if r.exists():
            return r[0]
        else:
            return None

    def instagram(self):
        r = InstagramAccount.objects.filter(user=self)
        if r.exists():
            return r[0]
        else:
            return None

    def feed(self):
        r = UserFeed.objects.filter(user=self)
        if r.exists():
            return r[0]
        else:
            return None
