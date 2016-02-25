import unittest
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from spokehub.invite.views import new_token
from spokehub.invite.models import Invite


class TestNewToken(unittest.TestCase):
    def test_length(self):
        n = new_token()
        self.assertEqual(len(n), 20)


class TestSignupView(TestCase):
    def setUp(self):
        self.c = Client()

    def test_no_token(self):
        r = self.c.get(reverse('invite_signup_form', args=['asdfasdf']))
        self.assertTrue("sorry" in r.content)


class TestInviteView(TestCase):
    def setUp(self):
        self.c = Client()

    def test_get(self):
        r = self.c.get("/invite/")
        self.assertEqual(r.status_code, 200)

    def test_post(self):
        r = self.c.post("/invite/", data=dict(email='foo@example.com'))
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Invite.objects.count(), 1)
        i = Invite.objects.all().first()
        self.assertEqual(i.status, 'OPEN')
        # now if we get the signup page with the token it should be ok
        r = self.c.get(reverse('invite_signup_form', args=[i.token]))
        self.assertTrue("Join" in r.content)
