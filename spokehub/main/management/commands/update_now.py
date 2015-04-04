from django.core.management.base import BaseCommand
from spokehub.twitter import hashtag_search as twitter_hashtag_search
from spokehub.instagram import hashtag_search as instagram_hashtag_search
from spokehub.tumblr import hashtag_search as tumblr_hashtag_search


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **kwargs):
        tumblr_hashtag_search()
        twitter_hashtag_search()
        instagram_hashtag_search()
