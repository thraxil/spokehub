from django.test import TestCase
from .factories import UserFactory, ItemFactory
from spokehub.main.models import Item


class ItemTest(TestCase):
    def test_get_absolute_url(self):
        i = ItemFactory()
        self.assertTrue(i.get_absolute_url().startswith('/item/'))

    def test_unicode(self):
        i = ItemFactory()
        self.assertTrue(str(i), "foo")

    def test_touch(self):
        i = ItemFactory()
        modified = i.modified
        i.touch()
        i2 = Item.objects.get(id=i.id)
        self.assertTrue(i2.modified > modified)

    def test_add_reply(self):
        u = UserFactory()
        i = ItemFactory()
        i.add_reply(u, 'a body')
        self.assertEqual(i.reply_set.all().count(), 1)
