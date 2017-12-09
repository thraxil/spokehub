from django.core import mail
from django.test import TestCase
from django.urls import reverse
from spokehub.main.tests.factories import UserFactory


class BroadcastViewTest(TestCase):
    def test_get(self):
        r = self.client.get(reverse('broadcast', args=[]))
        self.assertEqual(r.status_code, 200)

    def test_post(self):
        UserFactory()
        r = self.client.post(
            reverse('broadcast', args=[]),
            {
                'subject': 'cat',
                'body': 'kitty cat',
            }
        )
        self.assertEqual(r.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
