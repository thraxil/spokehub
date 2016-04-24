from django.core.management.base import BaseCommand
from spokehub.twitter import hashtag_search as twitter_hashtag_search
from spokehub.twitter import my_tweets
from spokehub.instagram import hashtag_search as instagram_hashtag_search
from spokehub.instagram import my_posts
from spokehub.tumblr import hashtag_search as tumblr_hashtag_search
from instagram.client import InstagramAPI
from django.conf import settings
import pytumblr


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **kwargs):
        my_tweets()
        tumblr_client = pytumblr.TumblrRestClient(
            settings.TUMBLR_CONSUMER_KEY,
            settings.TUMBLR_CONSUMER_SECRET,
            settings.TUMBLR_OAUTH_TOKEN,
            settings.TUMBLR_OAUTH_SECRET,
        )
        tumblr_hashtag_search(tumblr_client)
        twitter_hashtag_search()
        my_posts(InstagramAPI(access_token=settings.SH_INSTAGRAM_ACCESS_TOKEN))
        instagram_hashtag_search(
            InstagramAPI(access_token=settings.TH_INSTAGRAM_ACCESS_TOKEN))
