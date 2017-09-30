from django.core.management.base import BaseCommand
from spokehub.twitter import hashtag_search as twitter_hashtag_search
from spokehub.instagram import hashtag_scrape as instagram_hashtag_scrape
from spokehub.instagram import my_posts_scrape
from django.conf import settings
import tweepy


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **kwargs):
        CONSUMER_KEY = settings.TWITTER_API_KEY
        CONSUMER_SECRET = settings.TWITTER_API_SECRET
        ACCESS_KEY = settings.TWITTER_OAUTH_TOKEN
        ACCESS_SECRET = settings.TWITTER_OAUTH_VERIFIER

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth)

        twitter_hashtag_search(api, settings.HASHTAG)

        my_posts_scrape()
        instagram_hashtag_scrape()
