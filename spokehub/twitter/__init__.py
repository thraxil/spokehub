import tweepy
from django.conf import settings
from ..main.models import NowPost


def hashtag_search():
    CONSUMER_KEY = settings.TWITTER_API_KEY
    CONSUMER_SECRET = settings.TWITTER_API_SECRET
    ACCESS_KEY = settings.TWITTER_OAUTH_TOKEN
    ACCESS_SECRET = settings.TWITTER_OAUTH_VERIFIER

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    search_text = "#erlang"

    max_tweets = 20
    for t in tweepy.Cursor(api.search, q=search_text).items(max_tweets):
        print("@" + t.user.screen_name)
        print(t.text)
        r = NowPost.objects.filter(
            service='twitter',
            service_id=t.id_str)
        if r.exists():
            print "existing twitter post"
            continue

        try:
            np = NowPost.objects.create(
                screen_name=t.user.screen_name,
                service='twitter',
                service_id=t.id_str,
                text=t.text,
                created=t.created_at.isoformat(),
                original=t._json,
                )
            print(t.created_at.isoformat())
            print("new twitter post added")
            print(np.id)
        except Exception, e:
            print "failed with exception: " + str(e)
        # if hasattr(t, 'extended_entities'):
        #     ee = t.extended_entities
        #     if 'media' not in ee:
        #         continue
        #     if len(ee['media']) < 1:
        #         continue
        #     np.image_url = ee['media'][0]['media_url']
        #     np.image_width = ee['media'][0]['sizes']['small']['w']
        #     np.image_height = ee['media'][0]['sizes']['small']['h']
        #     np.save()
        #     print "added an image"
