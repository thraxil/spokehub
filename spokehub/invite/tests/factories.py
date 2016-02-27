import factory
from spokehub.invite.models import Invite


class InviteFactory(factory.DjangoModelFactory):
    class Meta:
        model = Invite
    email = "foo@example.com"
    token = "testtoken"
