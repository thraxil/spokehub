import factory
from factory.django import DjangoModelFactory
from spokehub.invite.models import Invite


class InviteFactory(DjangoModelFactory):
    class Meta:
        model = Invite
    email = "foo@example.com"
    token = "testtoken"
