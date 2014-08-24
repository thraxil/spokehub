from django.db import models
from django.contrib.auth.models import User
import tweepy
from django.conf import settings
from json import dumps
from ..main.models import NowPost


class TwitterAccount(models.Model):
    user = models.ForeignKey(User)
    oauth_token = models.TextField(blank=True, default='')
    oauth_verifier = models.TextField(blank=True, default='')
    screen_name = models.TextField(blank=True, default='')
    profile_image_url = models.TextField(blank=True, default='')

    def twitter_api(self):
        auth = tweepy.OAuthHandler(
            settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET)
        auth.set_access_token(self.oauth_token, self.oauth_verifier)
        return tweepy.API(auth)

    def update_details(self):
        """ fill in screen name and profile image """
        api = self.twitter_api()
        tw_user = api.me()
        self.screen_name = tw_user.screen_name
        self.profile_image_url = tw_user.profile_image_url
        self.save()

    def fetch_recent_posts(self):
        api = self.twitter_api()
        for t in api.user_timeline():
            r = NowPost.objects.filter(
                user=self.user,
                service='twitter',
                service_id=t.id_str)
            if r.exists():
                print "existing twitter post"
                continue
            np = NowPost.objects.create(
                user=self.user,
                service='twitter',
                service_id=t.id_str,
                text=t.text,
                created=t.created_at.isoformat(),
                original=dumps(
                    dict(
                        author_name=t.author.name,
                        author_screen_name=t.author.screen_name,
                        created_at=t.created_at.isoformat(),
                        id=t.id,
                        place=t.place,
                        source=t.source,
                        source_url=t.source_url,
                        retweet_count=t.retweet_count,
                        )
                    )
                )
            print t.created_at.isoformat()
            print str(np.created)
            print "new twitter post added"
