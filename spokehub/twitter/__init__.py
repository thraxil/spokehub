import tweepy
from django.conf import settings


def add_tweet(t):
    from ..main.models import NowPost
    r = NowPost.objects.filter(
        service='twitter',
        service_id=t.id_str)
    if r.exists():
        print "existing twitter post"
        return

    try:
        np = NowPost.objects.create_twitter(
            screen_name=t.user.screen_name,
            service_id=t.id_str,
            text=t.text,
            created=t.created_at.isoformat(),
            original_json=t._json,
        )
        print(t.created_at.isoformat())
        print("new twitter post added")
        print(np.id)
        process_extended_attributes(t, np)
    except Exception, e:
        print "failed with exception: " + str(e)


def process_extended_attributes(t, np):
    if hasattr(t, 'extended_entities'):
        ee = t.extended_entities
        if 'media' not in ee:
            return
        if len(ee['media']) < 1:
            return
        np.image_url = ee['media'][0]['media_url']
        np.image_width = ee['media'][0]['sizes']['large']['w']
        np.image_height = ee['media'][0]['sizes']['large']['h']
        np.save()
        print "added an image"


def my_tweets():
    CONSUMER_KEY = settings.TWITTER_API_KEY
    CONSUMER_SECRET = settings.TWITTER_API_SECRET
    ACCESS_KEY = settings.TWITTER_OAUTH_TOKEN
    ACCESS_SECRET = settings.TWITTER_OAUTH_VERIFIER
    USER = settings.TWITTER_USER

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    for t in api.user_timeline(USER):
        print("@" + t.user.screen_name)
        add_tweet(t)


def hashtag_search():
    CONSUMER_KEY = settings.TWITTER_API_KEY
    CONSUMER_SECRET = settings.TWITTER_API_SECRET
    ACCESS_KEY = settings.TWITTER_OAUTH_TOKEN
    ACCESS_SECRET = settings.TWITTER_OAUTH_VERIFIER

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    search_text = settings.HASHTAG

    max_tweets = 20
    for t in tweepy.Cursor(api.search, q=search_text).items(max_tweets):
        print("@" + t.user.screen_name)
        add_tweet(t)
