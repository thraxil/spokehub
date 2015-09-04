from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from waffle.models import Flag
from .factories import (UserFactory, ConversationFactory)


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

    def test_root_with_conversation(self):
        i = ConversationFactory()
        r = self.c.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(i.title in r.content)

    def test_userpage(self):
        r = self.c.get("/accounts/" + self.u.username + "/")
        self.assertEqual(r.status_code, 200)

    def test_add_conversation(self):
        r = self.c.post("/conversation/add/", dict(title='foo', body='bar'))
        self.assertEqual(r.status_code, 302)
        r = self.c.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertTrue('foo' in r.content)

    def test_reploy_to_conversation(self):
        Flag.objects.create(name="main", everyone=True)
        i = ConversationFactory()
        r = self.c.post(
            "/conversation/%d/reply/" % i.id,
            dict(
                title='reply title',
                body='reply body',
                url='http://foo.example.com/'),
        )
        self.assertEqual(r.status_code, 302)
        r = self.c.get("/")
        self.assertTrue('reply title' in r.content)
        self.assertTrue('reply body' in r.content)
        self.assertTrue('http://foo.example.com/' in r.content)

    @override_settings(MEDIA_ROOT="/tmp/")
    def test_reply_to_conversaion_with_image(self):
        Flag.objects.create(name="main", everyone=True)
        c = ConversationFactory()
        with open('spokehub/main/tests/bullet.gif') as img:
            r = self.c.post(
                "/conversation/%d/reply/" % c.id,
                dict(
                    title='reply title',
                    body='reply body',
                    url='http://foo.example.com/',
                    image=img,
                ),
            )
            self.assertEqual(r.status_code, 302)
