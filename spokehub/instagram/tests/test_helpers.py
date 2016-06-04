import unittest
from datetime import datetime
from spokehub.instagram import (
    image_image_url, add_post, add_media,
    my_posts,
)
from spokehub.instagram.scrape import (
    get_script, parse_json, entries, owner, clean_url,
    Entry,
)


class Dummy(object):
    pass


class DummyAPI(object):
    def user_recent_media(self):
        return ([], None)

    def tag_recent_media(self, **kwargs):
        return ([], None)


class TestImageURL(unittest.TestCase):
    def test_image(self):
        d = Dummy()
        d.type = "image"
        self.assertEqual(image_image_url(d, "foo"), "foo")

    def test_not_image(self):
        d = Dummy()
        d.type = "not image"
        self.assertEqual(image_image_url(d, "foo"), "")


class TestAddPost(unittest.TestCase):
    def test_invalid(self):
        d = Dummy()
        d.link = None
        self.assertIsNone(add_post(d))


class TestAddPosts(unittest.TestCase):
    def test_invalid(self):
        d = Dummy()
        d.link = None
        self.assertIsNone(add_media([d]))


class TestMyPosts(unittest.TestCase):
    def test_my_posts(self):
        api = DummyAPI()
        self.assertIsNone(my_posts(api))


sample_entry = {
    'caption': 'caption',
    'code': 'code',
    'comments': 'comments',
    'date': 1460935243,
    'dimensions': 'dimensions',
    'display_src': 'display_src',
    'id': 'id',
    'is_video': False,
    'likes': 0,
    'owner': {'id': '123'},
    'thumbnail_src': 'thumbnail_src',
}

emoji_json_entry = """{"code": "BGOkQ8oCKmG", "date": 1465032652,
 "dimensions": {"width": 1080, "height": 1080},
 "comments": {"count": 0},
 "caption": "#German #advertising is rarely notable,
 let alone perfect \ud83c\udf1f\ud83d\udc4f\ud83c\udffe. #spokehubnow",
 "likes": {"count": 8},
 "owner": {"id": "1456410553"},
 "thumbnail_src": "https://scontent-lhr3-1.cdninstagram.com/n.jpg",
 "is_video": false,
 "id": "1265108039619881350",
 "display_src": "https://scontent-lhr3-1.cdninstagram.com/n.jpg"}
"""

emoji_json = (
    """{"entry_data": {"TagPage": """
    """[{"tag": {"media": {"nodes": [%s]}}}]}}""" % emoji_json_entry
).replace('\n', '').replace('\r', '')


class TestScraper(unittest.TestCase):
    def test_get_script(self):
        html = ""
        r = get_script(html)
        self.assertIsNone(r)

        html = "<script>not me</script>"
        r = get_script(html)
        self.assertIsNone(r)

        html = "<script>window._sharedData = foo;</script>"
        r = get_script(html)
        self.assertEqual(r, "window._sharedData = foo;")

    def test_parse_json(self):
        s = """window._sharedData = {};"""
        d = parse_json(s)
        self.assertEqual(d, dict())

    def test_entries(self):
        d = {'entry_data': {'TagPage': [{'tag': {'media': {'nodes': 'foo'}}}]}}
        self.assertEqual(entries(d), 'foo')

    def test_owner(self):
        d = {'entry_data': {'PostPage': [{'media': {'owner': 'foo'}}]}}
        self.assertEqual(owner(d), 'foo')

    def test_clean_url(self):
        u = "http://foo.com/path?query=blah"
        self.assertEqual(clean_url(u), "http://foo.com/path")

    def test_emoji_parse(self):
        s = "window._sharedData = {};".format(emoji_json)
        d = parse_json(s)
        e = entries(d)
        self.assertEqual(len(e), 1)
        entry = Entry(e[0])
        self.assertEqual(entry.code, "BGOkQ8oCKmG")

    def test_entry_init(self):
        e = Entry(sample_entry)
        self.assertEqual(e.code, 'code')

    def test_entry_url(self):
        e = Entry(sample_entry)
        self.assertEqual(e.url(), "https://www.instagram.com/p/code/")

    def test_entry_date(self):
        e = Entry(sample_entry)
        self.assertEqual(e.date, datetime.fromtimestamp(1460935243))

    def test_entry_clean_display_src(self):
        pass

    def test_entry_clean_thumbnail_src(self):
        pass

    def test_entry_populate_owner(self):
        pass

    def test_entry_username(self):
        e = Entry(sample_entry)
        e._username = "username"
        self.assertEqual(e.username(), "username")

    def test_entry_fullname(self):
        e = Entry(sample_entry)
        e._fullname = "fullname"
        self.assertEqual(e.fullname(), "fullname")
