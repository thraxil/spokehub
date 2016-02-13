from django.conf import settings
import pytumblr
import json
from datetime import datetime
from ..main.models import NowPost


def add_post(i):
    url = i['short_url']
    r = NowPost.objects.filter(service='tumblr', service_id=url)
    ptype = i['type']
    if ptype not in ['photo', 'video', 'audio']:
        return
    if r.exists():
        print "existing tumblr post"
        return
    try:
        original = json.dumps(i)
        screen_name = i['blog_name']
        text = ""
        created = datetime.strptime(i['date'], '%Y-%m-%d %H:%M:%S %Z')
        image_url = ""
        image_width = 0
        image_height = 0
        if i['type'] == 'photo':
            if len(i['photos']) < 1:
                return
            p = i['photos'][0]
            image_url = p['original_size']['url']
            image_width = p['original_size']['width']
            image_height = p['original_size']['height']
            text = i['caption']
        text = video_text(ptype, i, text)
        text = audio_text(ptype, i, text)
        NowPost.objects.create_tumblr(
            screen_name=screen_name,
            service_id=url,
            text=text,
            created=created,
            image_url=image_url,
            image_width=image_width,
            image_height=image_height,
            original_json=original,
        )
        print("new tumblr post added")
    except Exception, e:
        print(str(e))


def video_text(ptype, i, text):
    if ptype == 'video':
        return i['player'][-1]['embed_code']
    return text


def audio_text(ptype, i, text):
    if ptype == 'audio':
        text = i['player']
    return text


def hashtag_search():
    client = pytumblr.TumblrRestClient(
        settings.TUMBLR_CONSUMER_KEY,
        settings.TUMBLR_CONSUMER_SECRET,
        settings.TUMBLR_OAUTH_TOKEN,
        settings.TUMBLR_OAUTH_SECRET,
    )
    posts = client.tagged(settings.HASHTAG)
    for i in posts:
        add_post(i)
