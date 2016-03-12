from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from waffle.testutils import override_flag
from .factories import (UserFactory, ConversationFactory, ReplyFactory)


class BasicTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_root(self):
        response = self.c.get("/")
        self.assertEquals(response.status_code, 200)

    def test_root_paginator(self):
        response = self.c.get("/?page=5")
        self.assertEquals(response.status_code, 200)

    def test_smoketest(self):
        response = self.c.get("/smoketest/")
        self.assertEquals(response.status_code, 200)


class LoggedInTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.u = UserFactory()
        self.u.set_password('test')
        self.u.save()
        self.c.login(username=self.u.username, password='test')

    def test_root(self):
        r = self.c.get("/")
        self.assertEqual(r.status_code, 200)

    @override_flag("main", True)
    def test_root_with_conversation(self):
        i = ConversationFactory()
        r = self.c.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(i.body in r.content)

    def test_userpage(self):
        r = self.c.get("/accounts/" + self.u.username + "/")
        self.assertEqual(r.status_code, 200)

    @override_flag("main", True)
    def test_add_conversation(self):
        r = self.c.post("/we/ask/", dict(body='bar'))
        self.assertEqual(r.status_code, 302)
        r = self.c.get("/we/")
        self.assertEqual(r.status_code, 200)
        self.assertTrue('foo' in r.content)

    @override_flag("main", True)
    def test_reploy_to_conversation(self):
        i = ConversationFactory()
        r = self.c.post(
            "/conversation/%d/reply/" % i.id,
            dict(
                body='reply body',
                url='http://foo.example.com/'),
        )
        self.assertEqual(r.status_code, 302)
        r = self.c.get(i.get_absolute_url())
        self.assertTrue('reply body' in r.content)
        self.assertTrue('http://foo.example.com/' in r.content)

    @override_settings(MEDIA_ROOT="/tmp/")
    @override_flag("main", True)
    def test_reply_to_conversaion_with_image(self):
        c = ConversationFactory()
        with open('media/img/bullet.gif') as img:
            r = self.c.post(
                "/conversation/%d/reply/" % c.id,
                dict(
                    body='reply body',
                    url='http://foo.example.com/',
                    image=img,
                ),
            )
            self.assertEqual(r.status_code, 302)

    def test_edit_reply(self):
        u = UserFactory()
        reply = ReplyFactory(author=u)
        r = self.c.get(reverse('edit-reply', args=[reply.id]))
        self.assertEqual(r.status_code, 200)


class TestUserProfiles(TestCase):
    def setUp(self):
        self.c = Client()

    def test_profile_view(self):
        u = UserFactory()
        r = self.c.get("/accounts/" + u.username + "/")
        self.assertEqual(r.status_code, 200)
