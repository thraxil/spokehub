import unittest
from spokehub.instagram import (
    image_image_url, add_post, add_media, hashtag_search,
    my_posts,
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


class TestHashTagSearch(unittest.TestCase):
    def test_hashtag_search(self):
        api = DummyAPI()
        self.assertIsNone(hashtag_search(api))


class TestMyPosts(unittest.TestCase):
    def test_my_posts(self):
        api = DummyAPI()
        self.assertIsNone(my_posts(api))
