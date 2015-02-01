from django.test import TestCase
from django.test.client import Client
from .factories import (UserFactory, ItemFactory)


class BasicTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_root(self):
        response = self.c.get("/")
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

    def test_root_with_item(self):
        i = ItemFactory()
        r = self.c.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(i.title in r.content)

    def test_userpage(self):
        r = self.c.get("/accounts/" + self.u.username + "/")
        self.assertEqual(r.status_code, 200)

    def test_add_item(self):
        r = self.c.post("/item/add/", dict(title='foo', body='bar'))
        self.assertEqual(r.status_code, 302)
        r = self.c.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertTrue('foo' in r.content)

    def test_reploy_to_item(self):
        i = ItemFactory()
        r = self.c.post(
            "/item/%d/reply/" % i.id,
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
