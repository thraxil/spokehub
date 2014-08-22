from django.db import models
from django.contrib.auth.models import User


class TwitterAccount(models.Model):
    user = models.ForeignKey(User)
    oauth_token = models.TextField(blank=True, default='')
    oauth_verifier = models.TextField(blank=True, default='')
    screen_name = models.TextField(blank=True, default='')
    profile_image_url = models.TextField(blank=True, default='')
