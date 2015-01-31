import factory

from django.contrib.auth.models import User
from spokehub.main.models import Item


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = "testuser"
    email = "test@example.com"


class ItemFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Item
    title = 'foo'
