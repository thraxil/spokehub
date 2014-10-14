from django.core.management.base import BaseCommand
from spokehub.twitter.models import TwitterAccount
from spokehub.instagram.models import InstagramAccount
from spokehub.feed.models import UserFeed


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **kwargs):
        for ta in TwitterAccount.objects.all():
            ta.fetch_recent_posts()
        for ta in InstagramAccount.objects.all():
            ta.fetch_recent_posts()
        for ta in UserFeed.objects.all():
            ta.fetch_recent_posts()
