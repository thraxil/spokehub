from django.test import TestCase
from .factories import UserFactory, ItemFactory


class ItemTest(TestCase):
    def test_get_absolute_url(self):
        i = ItemFactory()
        self.assertTrue(i.get_absolute_url().startswith('/item/'))

    def test_touch(self):
        i = ItemFactory()
        i.touch()

    def test_add_reply(self):
        u = UserFactory()
        i = ItemFactory()
        i.add_reply(u, 'a body')
