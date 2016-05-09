import unittest
from django.test import TestCase
from spokehub.tumblr import video_text, audio_text, add_post, photo_params


class TestHelpers(unittest.TestCase):
    def test_video_text_nonvideo(self):
        r = video_text('something', None, 'some text')
        self.assertEqual(r, 'some text')

    def test_video_text_video(self):
        d = {'player': [{'embed_code': 'an embed code'}]}
        r = video_text('video', d, 'some text')
        self.assertEqual(r, 'an embed code')

    def test_audio_text_nonaudio(self):
        r = audio_text('something', None, 'some text')
        self.assertEqual(r, 'some text')

    def test_audio_text_video(self):
        d = {'player': 'some audio text'}
        r = audio_text('audio', d, 'some text')
        self.assertEqual(r, 'some audio text')

    def test_photo_params(self):
        d = {'type': 'not photo'}
        results = photo_params(d)
        self.assertEqual(results, ('', '', 0, 0))

        d = {
            'type': 'photo',
            'photos': [
                {
                    'original_size': {
                        'url': 'foo',
                        'width': 5,
                        'height': 7,
                    }
                }
            ],
            'caption': 'a caption',
        }
        results = photo_params(d)
        self.assertEqual(results, ('a caption', 'foo', 5, 7))


class TestAddPost(TestCase):
    def test_unknown_ptype(self):
        d = dict(short_url='foo', type='unknown')
        self.assertIsNone(add_post(d))

    def test_valid_ptype_but_otherwise_invalid(self):
        d = dict(short_url='foo', type='photo')
        self.assertIsNone(add_post(d))
