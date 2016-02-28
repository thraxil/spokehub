import unittest
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from spokehub.invite.views import new_token
from spokehub.invite.models import Invite
from .factories import InviteFactory


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

    def test_post_no_token(self):
        r = self.c.post(reverse('invite_signup_form', args=['asdfasdf']))
        self.assertTrue("sorry" in r.content)

    def test_get_valid_token(self):
        i = InviteFactory()
        r = self.c.get(reverse("invite_signup_form", args=[i.token]))
        self.assertTrue("password" in r.content)

    def test_post(self):
        i = InviteFactory()
        r = self.c.post(reverse("invite_signup_form", args=[i.token]),
                        data=dict(
                            password1='pass',
                            password2='pass',
                            username='newuser',
                            firstname='first',
                            lastname='last',
                            website='http://example.com/',
                            websitename='awesome site',
                            profession='anarchist',
                            email=i.email,
                        ))
        # should make a new user with the appropriate fields
        u = User.objects.filter(username='newuser', email=i.email,
                                first_name='first', last_name='last')
        self.assertEqual(u.count(), 1)

        # should make a new profile
        self.assertEqual(u.first().profile.website_url, 'http://example.com/')
        self.assertEqual(u.first().profile.profession, 'anarchist')
        self.assertEqual(u.first().profile.website_name, 'awesome site')

        # should clear out the invite so it can't be reused
        self.assertEqual(Invite.objects.filter(token=i.token).count(), 0)

        # should redirect to user profile edit page
        self.assertEqual(r.status_code, 302)

    def test_post_with_profileimage(self):
        i = InviteFactory()
        with open('media/img/bullet.gif') as img:
            r = self.c.post(
                reverse("invite_signup_form", args=[i.token]),
                data=dict(
                    password1='pass',
                    password2='pass',
                    username='newuser',
                    firstname='first',
                    lastname='last',
                    website='http://example.com/',
                    websitename='awesome site',
                    profession='anarchist',
                    email=i.email,
                    profileimage=img,
                ))

            self.assertEqual(r.status_code, 302)
            # should make a new user with the appropriate fields
            u = User.objects.filter(username='newuser', email=i.email,
                                    first_name='first', last_name='last')
            self.assertEqual(u.count(), 1)
            self.assertNotEqual(u.first().profile.get_mugshot_url(), '')


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
        self.assertTrue("password" in r.content)
