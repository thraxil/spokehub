from django.contrib.auth.models import User
from django import template

register = template.Library()


class DummyUser(object):
    def __init__(self):
        self.dummy = True

    def fullname(self):
        return "dummy user"


@register.simple_tag
def user_profile(username):
    try:
        print(username)
        u = User.objects.get(username=username)
        return u
    except User.DoesNotExist:
        return DummyUser()
