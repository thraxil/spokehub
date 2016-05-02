from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
from waffle.testutils import override_flag
from .factories import (UserFactory, ConversationFactory, ReplyFactory)


class BasicTest(TestCase):
    def test_root(self):
        response = self.client.get("/")
        self.assertEquals(response.status_code, 200)

    def test_root_paginator(self):
        response = self.client.get("/?page=5")
        self.assertEquals(response.status_code, 200)

    def test_smoketest(self):
        response = self.client.get("/smoketest/")
        self.assertEquals(response.status_code, 200)


class LoggedInTest(TestCase):
    def setUp(self):
        self.u = UserFactory()
        self.u.set_password('test')
        self.u.save()
        self.client.login(username=self.u.username, password='test')

    def test_root(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)

    @override_flag("main", True)
    def test_root_with_conversation(self):
        i = ConversationFactory()
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(i.body in r.content)

    def test_userpage(self):
        r = self.client.get("/accounts/" + self.u.username + "/")
        self.assertEqual(r.status_code, 200)

    @override_flag("main", True)
    def test_add_conversation(self):
        r = self.client.post("/we/ask/", dict(body='bar'))
        self.assertEqual(r.status_code, 302)
        r = self.client.get("/we/")
        self.assertEqual(r.status_code, 200)
        self.assertTrue('foo' in r.content)

    @override_flag("main", True)
    def test_conversation_archive(self):
        c = ConversationFactory()
        r = self.client.get(reverse('we-archive'))
        self.assertEqual(r.status_code, 200)
        self.assertTrue(c.body in r.content)

    @override_flag("main", True)
    def test_reploy_to_conversation(self):
        i = ConversationFactory()
        r = self.client.post(
            "/conversation/%d/reply/" % i.id,
            dict(
                body='reply body',
                url='http://foo.example.com/'),
        )
        self.assertEqual(r.status_code, 302)
        r = self.client.get(i.get_absolute_url())
        self.assertTrue('reply body' in r.content)
        self.assertTrue('http://foo.example.com/' in r.content)

    @override_flag("main", True)
    @override_flag("comments", True)
    def test_add_comment(self):
        reply = ReplyFactory()
        r = self.client.post(
            reverse('add-comment', args=[reply.id]),
            dict(body="a new comment"))
        self.assertEqual(r.status_code, 302)
        r = self.client.get(reply.item.get_absolute_url())
        self.assertTrue('a new comment' in r.content)

    @override_settings(MEDIA_ROOT="/tmp/")
    @override_flag("main", True)
    def test_reply_to_conversaion_with_image(self):
        c = ConversationFactory()
        with open('media/img/bullet.gif') as img:
            r = self.client.post(
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
        r = self.client.get(reverse('edit-reply', args=[reply.id]))
        self.assertEqual(r.status_code, 200)

    def test_profile_index(self):
        UserFactory()
        r = self.client.get("/accounts/")
        self.assertEqual(r.status_code, 200)


class TestUserProfiles(TestCase):
    def test_profile_view(self):
        u = UserFactory()
        r = self.client.get("/accounts/" + u.username + "/")
        self.assertEqual(r.status_code, 200)

    def test_profile_index(self):
        UserFactory()
        r = self.client.get("/accounts/")
        self.assertEqual(r.status_code, 302)
