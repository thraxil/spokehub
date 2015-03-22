from instagram.client import InstagramAPI
from django.conf import settings
from ..main.models import NowPost
from json import dumps


def hashtag_search():
    api = InstagramAPI(access_token=settings.INSTAGRAM_ACCESS_TOKEN)

    # instagram wants it without the hashtag
    tag_name = settings.HASHTAG.strip('#')

    recent_media, n = api.tag_recent_media(tag_name=tag_name)
    for media in recent_media:
        r = NowPost.objects.filter(
            service='instagram',
            service_id=media.link)
        if r.exists():
            print("existing instagram post")
            continue
        try:
            sru = media.get_standard_resolution_url()
            try:
                text = media.caption.text
            except:
                text = ""

            media_url = media.get_standard_resolution_url()
            image_url = ""
            video_url = ""

            if media.type == 'image':
                # all we can handle right now
                image_url = media_url
            if media.type == 'video':
                video_url = media_url

            NowPost.objects.create(
                screen_name=media.user.username,
                service='instagram',
                service_id=media.link,
                text=text,
                created=media.created_time.isoformat(),
                image_url=image_url,
                video_url=video_url,
                image_width=640,
                image_height=640,
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
            print "new instagram post added"
        except Exception, e:
            print "failed with exception: " + str(e)
