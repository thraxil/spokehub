import factory

from django.contrib.auth.models import User
from spokehub.main.models import Conversation, Reply


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: 'user{0}'.format(n))
    email = factory.Sequence(lambda n: 'user{0}@example.com'.format(n))


class ConversationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Conversation
    title = 'foo'


class ReplyFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Reply
    item = factory.SubFactory(ConversationFactory)
    author = factory.SubFactory(UserFactory)
    body = "reply body"
    title = "reply title"
