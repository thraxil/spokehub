from django.conf import settings
import json
from datetime import datetime
from django_statsd.clients import statsd
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
        _add_post(ptype, url, i)
        statsd.incr('tumblr.add.success')
    except Exception, e:
        print(str(e))
        statsd.incr('tumblr.add.failed')


def _add_post(ptype, url, i):
    original = json.dumps(i)
    screen_name = i['blog_name']
    created = datetime.strptime(i['date'], '%Y-%m-%d %H:%M:%S %Z')
    (text, image_url, image_width, image_height) = photo_params(i)
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


def photo_params(i):
    text = ""
    image_url = ""
    image_width = 0
    image_height = 0
    if i['type'] == 'photo':
        p = i['photos'][0]
        image_url = p['original_size']['url']
        image_width = p['original_size']['width']
        image_height = p['original_size']['height']
        text = i['caption']
    return (text, image_url, image_width, image_height)


def video_text(ptype, i, text):
    if ptype == 'video':
        return i['player'][-1]['embed_code']
    return text


def audio_text(ptype, i, text):
    if ptype == 'audio':
        text = i['player']
    return text


def hashtag_search(client):
    posts = client.tagged(settings.HASHTAG)
    for i in posts:
        add_post(i)
    statsd.incr('tumblr.hashtag.run')
