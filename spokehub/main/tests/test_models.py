from django.test import TestCase
from django.contrib.auth.models import User
from spokehub.main.models import Item


class ItemTest(TestCase):
    def test_get_absolute_url(self):
        i = Item.objects.create(title='foo')
        self.assertTrue(i.get_absolute_url().startswith('/item/'))

    def test_touch(self):
        i = Item.objects.create(title='foo')
        i.touch()

    def test_add_reply(self):
        u = User.objects.create(username='test')
        i = Item.objects.create(title='foo')
        i.add_reply(u, 'a body')
