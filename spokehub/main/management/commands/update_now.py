from django.core.management.base import BaseCommand
from spokehub.twitter import hashtag_search as twitter_hashtag_search
from spokehub.instagram import hashtag_scrape as instagram_hashtag_scrape
from spokehub.instagram import my_posts_scrape
from spokehub.tumblr import hashtag_search as tumblr_hashtag_search
from django.conf import settings
import pytumblr
import time
import tweepy


class Command(BaseCommand):
    args = ''
    help = ''
    max_tries = 5

    def handle(self, *args, **kwargs):
        CONSUMER_KEY = settings.TWITTER_API_KEY
        CONSUMER_SECRET = settings.TWITTER_API_SECRET
        ACCESS_KEY = settings.TWITTER_OAUTH_TOKEN
        ACCESS_SECRET = settings.TWITTER_OAUTH_VERIFIER

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth)

        twitter_hashtag_search(api, settings.HASHTAG)

        tumblr_client = pytumblr.TumblrRestClient(
            settings.TUMBLR_CONSUMER_KEY,
            settings.TUMBLR_CONSUMER_SECRET,
            settings.TUMBLR_OAUTH_TOKEN,
            settings.TUMBLR_OAUTH_SECRET,
        )
        tumblr_hashtag_search(tumblr_client)

        tries = 0
        captured_exception = None
        while tries < self.max_tries:
            try:
                my_posts_scrape()
                instagram_hashtag_scrape()
                return
            except Exception as e:
                tries += 1
                time.sleep(2 ** tries)
                captured_exception = e
        raise captured_exception
