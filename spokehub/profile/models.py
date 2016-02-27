from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile


class Profile(UserenaBaseProfile):
    user = models.OneToOneField(
        User,
        unique=True,
        verbose_name=_('user'),
        related_name='profile')
    about_me = models.TextField(blank=True, default="")
    discipline1 = models.CharField(max_length=256, blank=True, default="")
    discipline2 = models.CharField(max_length=256, blank=True, default="")
    website_url = models.CharField(max_length=256, blank=True, default="")
    website_name = models.CharField(max_length=256, blank=True, default="")
    location = models.CharField(max_length=256, blank=True, default="")
