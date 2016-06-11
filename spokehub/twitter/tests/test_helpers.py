import unittest
from spokehub.twitter import (
    process_extended_attributes, add_tweet, ensure_https)


class Dummy(object):
    pass


class MockNP(object):
    def __init__(self):
        self.saved = False

    def save(self):
        self.saved = True


class TestProcessExtendedAttributes(unittest.TestCase):
    def test_no_ext_entities(self):
        m = MockNP()
        process_extended_attributes(None, m)
        self.assertFalse(m.saved)

    def test_no_media(self):
        m = MockNP()
        ee = dict()
        d = Dummy()
        d.extended_entities = ee
        process_extended_attributes(d, m)
        self.assertFalse(m.saved)
        ee = dict(media=[])
        d.extended_entities = ee
        process_extended_attributes(d, m)
        self.assertFalse(m.saved)

    def test_with_media(self):
        ee = dict(
            media=[
                {
                    'media_url': 'test',
                    'sizes': {'large': {'w': 400, 'h': 500}}
                }
            ])
        d = Dummy()
        d.extended_entities = ee
        m = MockNP()
        process_extended_attributes(d, m)
        self.assertTrue(m.saved)
        self.assertEqual(m.image_url, 'test')
        self.assertEqual(m.image_width, 400)
        self.assertEqual(m.image_height, 500)


class TestAddTweet(unittest.TestCase):
    def test_invalid(self):
        d = Dummy()
        d.link = None
        d.id_str = "foo"
        self.assertIsNone(add_tweet(d))


class TestEnsureHttps(unittest.TestCase):
    def test_http(self):
        url = "http://www.google.com/"
        self.assertEqual(ensure_https(url), "https://www.google.com/")

    def test_https(self):
        url = "https://i.dont.need.to.change.com/"
        self.assertEqual(ensure_https(url), url)
