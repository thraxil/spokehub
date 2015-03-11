from django.test import TestCase
from .factories import UserFactory, ConversationFactory, ReplyFactory
from spokehub.main.models import Conversation


class ConversationTest(TestCase):
    def test_get_absolute_url(self):
        i = ConversationFactory()
        self.assertTrue(i.get_absolute_url().startswith('/conversation/'))

    def test_unicode(self):
        i = ConversationFactory()
        self.assertTrue(str(i), "foo")

    def test_touch(self):
        i = ConversationFactory()
        modified = i.modified
        i.touch()
        i2 = Conversation.objects.get(id=i.id)
        self.assertTrue(i2.modified > modified)

    def test_add_reply(self):
        u = UserFactory()
        i = ConversationFactory()
        i.add_reply(u, 'a body')
        self.assertEqual(i.reply_set.all().count(), 1)

    def test_add_reply_no_author(self):
        i = ConversationFactory()
        i.add_reply(None, 'a body')
        self.assertEqual(i.reply_set.all().count(), 0)

    def test_add_reply_empty_body(self):
        i = ConversationFactory()
        u = UserFactory()
        i.add_reply(u, '')
        self.assertEqual(i.reply_set.all().count(), 0)

    def test_add_reply_fix_url(self):
        i = ConversationFactory()
        u = UserFactory()
        i.add_reply(u, 'a body', 'example.com')
        r = i.reply_set.all()[0]
        self.assertEqual(r.url, "http://example.com")

    def test_reply_pairs(self):
        i = ConversationFactory()
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


class ReplyTest(TestCase):
    def test_unicode(self):
        r = ReplyFactory()
        self.assertTrue(str(r).startswith("Reply to"))

    def test_mentioned_users(self):
        u = UserFactory()
        u2 = UserFactory()
        r = ReplyFactory(
            body="@nonexistent @%s @%s" % (u.username, u2.username),
            author=u2)
        self.assertEqual(r.mentioned_users(), [u])

    def test_conversation_users(self):
        r = ReplyFactory()
        self.assertEqual(len(r.conversation_users()), 0)
        ReplyFactory(item=r.item)
        self.assertEqual(len(r.conversation_users()), 1)
