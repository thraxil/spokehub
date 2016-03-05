from django.test import TestCase
from userena.utils import get_user_profile
from spokehub.main.tests.factories import UserFactory


class ProfileTest(TestCase):
    def test_completed(self):
        u = UserFactory()
        p = get_user_profile(u)
        self.assertFalse(p.completed())
        p.location = "a location"
        p.profession = "a profession"
        p.save()
        u.first_name = "first"
        u.last_name = "last"
        u.save()
        self.assertTrue(p.completed())

    def test_questions(self):
        u = UserFactory()
        p = get_user_profile(u)
        self.assertEqual(p.questions().count(), 0)

    def test_replies(self):
        u = UserFactory()
        p = get_user_profile(u)
        self.assertEqual(p.replies().count(), 0)

    def test_replied_to(self):
        u = UserFactory()
        p = get_user_profile(u)
        self.assertEqual(len(list(p.replied_to())), 0)
