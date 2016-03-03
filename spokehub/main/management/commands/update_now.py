from django.core.management.base import BaseCommand
from spokehub.twitter import hashtag_search as twitter_hashtag_search
from spokehub.twitter import my_tweets
from spokehub.instagram import hashtag_search as instagram_hashtag_search
from spokehub.instagram import my_posts
from spokehub.tumblr import hashtag_search as tumblr_hashtag_search


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **kwargs):
        my_tweets()
        tumblr_hashtag_search()
        twitter_hashtag_search()
        my_posts()
        instagram_hashtag_search()
