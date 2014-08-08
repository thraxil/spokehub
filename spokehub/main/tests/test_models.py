from django.test import TestCase
from django.contrib.auth.models import User
from spokehub.main.models import Item


class ItemTest(TestCase):
    def test_get_absolute_url(self):
        u = User.objects.create(username='test')
        i = Item.objects.create(author=u, title='foo', section='case')
        self.assertTrue(i.get_absolute_url().startswith('/case/'))

    def test_touch(self):
        u = User.objects.create(username='test')
        i = Item.objects.create(author=u, title='foo', section='case')
        i.touch()

    def test_add_reply(self):
        u = User.objects.create(username='test')
        i = Item.objects.create(author=u, title='foo', section='case')
        i.add_reply(u, 'a body')
