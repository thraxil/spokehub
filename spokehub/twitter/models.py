from django.db import models
from django.contrib.auth.models import User
import tweepy
from django.conf import settings


class TwitterAccount(models.Model):
    user = models.ForeignKey(User)
    oauth_token = models.TextField(blank=True, default='')
    oauth_verifier = models.TextField(blank=True, default='')
    screen_name = models.TextField(blank=True, default='')
    profile_image_url = models.TextField(blank=True, default='')

    def twitter_api(self):
        auth = tweepy.OAuthHandler(
            settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET)
        auth.set_access_token(self.oauth_token, self.oauth_verifier)
        return tweepy.API(auth)

    def update_details(self):
        """ fill in screen name and profile image """
        api = self.twitter_api()
        tw_user = api.me()
        self.screen_name = tw_user.screen_name
        self.profile_image_url = tw_user.profile_image_url
        self.save()
