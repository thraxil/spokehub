from django.contrib.auth.models import User
from django import template

register = template.Library()


class DummyUser(object):
    def __init__(self):
        self.dummy = True


@register.simple_tag
def user_profile(username):
    try:
        u = User.objects.get(username=username)
        return u
    except User.DoesNotExist:
        return DummyUser()


@register.inclusion_tag('userena/hover_link.html')
def hover_link(username, fullname):
    return dict(username=username, fullname=fullname)
