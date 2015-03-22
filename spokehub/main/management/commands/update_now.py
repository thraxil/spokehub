from django.core.management.base import BaseCommand
from spokehub.twitter import hashtag_search


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **kwargs):
        hashtag_search()
