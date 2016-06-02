from json import dumps
from django.conf import settings
from django_statsd.clients import statsd
from .scrape import (
    get_script, parse_json, entries, Entry
)
import requests


def add_post(media):
    from ..main.models import NowPost

    r = NowPost.objects.filter(
        service='instagram',
        service_id=media.link)
    if r.exists():
        print("existing instagram post")
        return
    try:
        _add_post(media, NowPost)
        statsd.incr('instagram.add.success')
    except Exception, e:
        print "failed with exception: " + str(e)
        statsd.incr('instagram.add.failed')


def add_scraped_post(media):
    from ..main.models import NowPost

    r = NowPost.objects.filter(
        service='instagram',
        service_id=media.url())
    if r.exists():
        print("existing instagram post")
        return
    try:
        _add_scraped_post(media, NowPost)
        statsd.incr('instagram.add.success')
    except Exception, e:
        print "failed with exception: " + str(e)
        statsd.incr('instagram.add.failed')


def _add_scraped_post(media, NowPost):
    sru = media.clean_display_src()
    try:
        text = media.caption
    except:
        text = ""

    video_url = ""
    image_url = sru

    NowPost.objects.create_instagram(
        media.username(), media.url(), text,
        media.date.isoformat(),
        image_url, video_url, dumps(
            dict(
                standard_resolution_url=sru,
                thumbnail_url=media.clean_thumbnail_src(),
                id=media.id,
                link=media.url(),
                user_id=media.owner,
                user_full_name=media.fullname(),
                user_username=media.username(),
                )
            )
    )
    print "new instagram post added"


def _add_post(media, NowPost):
    sru = media.get_standard_resolution_url()
    try:
        text = media.caption.text
    except:
        text = ""

    media_url = media.get_standard_resolution_url()
    video_url = ""

    image_url = image_image_url(media, media_url)
    if media.type == 'video':
        video_url = media_url

    NowPost.objects.create_instagram(
        media.user.username, media.link, text,
        media.created_time.isoformat(),
        image_url, video_url, dumps(
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
    print "new instagram post added"


def image_image_url(media, media_url):
    if media.type == 'image':
        # all we can handle right now
        return media_url
    return ""


def hashtag_scrape():
    tag_name = settings.HASHTAG.strip('#')

    url = "https://www.instagram.com/explore/tags/{}/".format(tag_name)
    r = requests.get(url)
    script = get_script(r.text)
    d = parse_json(script)
    entry_data = entries(d)
    for entry in entry_data:
        e = Entry(entry)
        if e.is_video:
            # can't handle video yet
            continue
        add_scraped_post(e)
    statsd.incr('instagram.hashtag.run')


def my_posts(api):
    recent_media, _ = api.user_recent_media()
    add_media(recent_media)
    statsd.incr('instagram.myposts.run')


def add_media(recent_media):
    for media in recent_media:
        add_post(media)
