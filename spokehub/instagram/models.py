from django.db import models
from django.contrib.auth.models import User
from instagram.client import InstagramAPI
from json import dumps
from ..main.models import NowPost


class InstagramAccount(models.Model):
    user = models.ForeignKey(User)
    access_token = models.TextField(blank=True, default='')
    screen_name = models.TextField(blank=True, default='')
    profile_image_url = models.TextField(blank=True, default='')

    def __unicode__(self):
        return "%s -> %s" % (self.user.username, self.screen_name)

    def update_details(self):
        pass

    def fetch_recent_posts(self):
        api = InstagramAPI(access_token=self.access_token)
        recent_media, n = api.user_recent_media()
        for media in recent_media:
            if media.type != 'image':
                # all we can handle right now
                continue
            r = NowPost.objects.filter(
                user=self.user,
                service='instagram',
                service_id=media.link)
            if r.exists():
                print "existing instagram post"
                continue
            try:
                sru = media.get_standard_resolution_url()
                try:
                    text = media.caption.text
                except:
                    text = ""
                np = NowPost.objects.create(
                    user=self.user,
                    service='instagram',
                    service_id=media.link,
                    text=text,
                    created=media.created_time.isoformat(),
                    image_url=media.get_low_resolution_url(),
                    image_width=306,
                    image_height=306,
                    original=dumps(
                        dict(
                            standard_resolution_url=sru,
                            thumbnail_url=media.get_thumbnail_url(),
                            id=media.id,
                            link=media.link,
                            filter=media.filter,
                            user_id=media.user.id,
                            user_full_name=media.user.full_name,
                            user_username=media.user.username,
                            )
                        )
                    )
                print media.created_time.isoformat()
                print str(np.created)
                print "new instagram post added"
            except Exception, e:
                print "failed with exception: " + str(e)
