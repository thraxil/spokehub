import tweepy
from django_statsd.clients import statsd


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
        statsd.incr('tweets.add.success')
    except Exception, e:
        print "failed with exception: " + str(e)
        statsd.incr('tweets.add.failed')


def process_extended_attributes(t, np):
    if hasattr(t, 'extended_entities'):
        ee = t.extended_entities
        if 'media' not in ee:
            return
        if len(ee['media']) < 1:
            return
        np.image_url = ensure_https(ee['media'][0]['media_url'])
        np.image_width = ee['media'][0]['sizes']['large']['w']
        np.image_height = ee['media'][0]['sizes']['large']['h']
        np.save()
        print "added an image"


def ensure_https(url):
    return url.replace("http://", "https://")


def my_tweets(api, user):
    # for t in api.user_timeline(user):
    #     print("@" + t.user.screen_name)
    #     add_tweet(t)
    statsd.incr('tweets.mytweets.run')


def hashtag_search(api, hashtag):
    search_text = hashtag

    max_tweets = 20
    for t in tweepy.Cursor(api.search, q=search_text).items(max_tweets):
        print("@" + t.user.screen_name)
        add_tweet(t)
    statsd.incr('tweets.hashtag.run')
