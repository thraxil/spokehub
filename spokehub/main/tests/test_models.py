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

    def test_add_reply_no_author(self):
        i = ItemFactory()
        i.add_reply(None, 'a body')
        self.assertEqual(i.reply_set.all().count(), 0)

    def test_add_reply_empty_body(self):
        i = ItemFactory()
        u = UserFactory()
        i.add_reply(u, '')
        self.assertEqual(i.reply_set.all().count(), 0)

    def test_add_reply_fix_url(self):
        i = ItemFactory()
        u = UserFactory()
        i.add_reply(u, 'a body', 'example.com')
        r = i.reply_set.all()[0]
        self.assertEqual(r.url, "http://example.com")

    def test_reply_pairs(self):
        i = ItemFactory()
        u = UserFactory()
        r = i.reply_pairs()
        self.assertEqual(len(r), 0)
        i.add_reply(u, 'a body')
        r = i.reply_pairs()
        self.assertEqual(len(r), 1)
        i.add_reply(u, 'another body')
        r = i.reply_pairs()
        self.assertEqual(len(r), 1)
        i.add_reply(u, 'third body')
        r = i.reply_pairs()
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0][0].body, "a body")
        self.assertEqual(r[0][1].body, "another body")
        self.assertEqual(r[1][0].body, "third body")
