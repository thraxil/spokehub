from django.core import mail
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from spokehub.contact.views import ContactView, ThanksView


class TestContactView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get(self):
        request = self.factory.get(reverse('contact_form'))
        response = ContactView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        request = self.factory.post(
            reverse('contact_form'),
            dict(name='someone', email='foo@foo.com', message='a message'))
        response = ContactView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)


class TestThanksView(TestCase):
    def test_get(self):
        factory = RequestFactory()
        request = factory.get(reverse('contact_thanks'))
        response = ThanksView.as_view()(request)
        self.assertEqual(response.status_code, 200)
