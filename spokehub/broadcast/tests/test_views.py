from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from spokehub.main.tests.factories import UserFactory


class BroadcastViewTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_get(self):
        r = self.c.get(reverse('broadcast', args=[]))
        self.assertEqual(r.status_code, 200)

    def test_post(self):
        UserFactory()
        r = self.c.post(
            reverse('broadcast', args=[]),
            {
                'subject': 'cat',
                'body': 'kitty cat',
            }
        )
        self.assertEqual(r.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
