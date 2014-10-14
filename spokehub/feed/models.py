from django.db import models
from django.contrib.auth.models import User
import feedparser
from datetime import datetime
from django.utils.timezone import utc
from time import mktime
from ..main.models import NowPost


def get_entry_guid(entry):
    """ get the guid for an entry

    prefer: 'guid', 'id', 'link'

    if it can't find any of those, None
    """
    return entry.get(
        'guid',
        entry.get(
            'id',
            entry.get('link', None)
        )
    )


class UserFeed(models.Model):
    user = models.ForeignKey(User)
    url = models.TextField(default="", blank=True)

    def __unicode__(self):
        return "feed for %s" % (self.user.username)

    def _import_entries(self, d):
        for entry in d.entries:
            guid = get_entry_guid(entry)
            if not guid:
                continue
            r = NowPost.objects.filter(
                user=self.user,
                service='feed',
                service_id=guid)
            if r.exists():
                print "existing feed entry"
                continue
            try:
                published = datetime.utcnow().replace(tzinfo=utc)
                if 'published_parsed' in entry:
                    published = datetime.fromtimestamp(
                        mktime(entry.published_parsed)).replace(tzinfo=utc)
                elif 'updated_parsed' in entry:
                    published = datetime.fromtimestamp(
                        mktime(entry.updated_parsed)).replace(tzinfo=utc)

                NowPost.objects.create(
                    user=self.user,
                    service='feed',
                    service_id=guid,
                    text=entry.get(
                        'description',
                        entry.get('summary', u"")),
                    created=published,
                    )
                print "new feed entry added"
            except Exception, e:
                print "failed with exception: " + str(e)

    def fetch_recent_posts(self):
        print "fetching %s" % self.url
        d = feedparser.parse(self.url)
        if 'status' in d and d.status == 404:
            return
        if 'status' in d and d.status == 410:
            return
        if 'entries' not in d:
            return
        self._import_entries(d)
