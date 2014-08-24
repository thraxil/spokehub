from django.core.management.base import BaseCommand
from spokehub.twitter.models import TwitterAccount


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **kwargs):
        for ta in TwitterAccount.objects.all():
            ta.fetch_recent_posts()
