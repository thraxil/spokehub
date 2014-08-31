from django.db import models
from django.contrib.auth.models import User


class InstagramAccount(models.Model):
    user = models.ForeignKey(User)
    access_token = models.TextField(blank=True, default='')
    screen_name = models.TextField(blank=True, default='')
    profile_image_url = models.TextField(blank=True, default='')

    def update_details(self):
        pass

    def fetch_recent_posts(self):
        pass
