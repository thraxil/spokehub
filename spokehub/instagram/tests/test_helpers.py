import unittest
from spokehub.instagram import image_image_url, add_post, add_media


class Dummy(object):
    pass


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
