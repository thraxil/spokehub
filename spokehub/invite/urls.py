from django.conf.urls import url
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Invite
from .views import InviteView, SignupView


urlpatterns = [
    url(r'^$', InviteView.as_view(), name='invite_form'),
    url(r'list/$', ListView.as_view(model=Invite), name='invite-list'),
    url(r'(?P<pk>\d+)/$', DetailView.as_view(model=Invite),
        name='invite-detail'),
    url(r'^signup/(?P<token>[^/]+)/$',
        SignupView.as_view(), name='invite_signup_form'),
]
