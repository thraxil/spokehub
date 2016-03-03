from instagram.client import InstagramAPI
from django.conf import settings
from json import dumps


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
    except Exception, e:
        print "failed with exception: " + str(e)


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


def hashtag_search():
    api = InstagramAPI(access_token=settings.TH_INSTAGRAM_ACCESS_TOKEN)

    # instagram wants it without the hashtag
    tag_name = settings.HASHTAG.strip('#')

    recent_media, n = api.tag_recent_media(tag_name=tag_name)
    for media in recent_media:
        add_post(media)


def my_posts():
    api = InstagramAPI(access_token=settings.SH_INSTAGRAM_ACCESS_TOKEN)
    recent_media, _ = api.user_recent_media()
    for media in recent_media:
        add_post(media)
