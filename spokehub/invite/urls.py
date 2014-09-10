from django.conf.urls import patterns, url
from .views import InviteView, SignupView


urlpatterns = patterns(
    '',
    url(r'^$', InviteView.as_view(), name='invite_form'),
    url(r'^signup/(?P<token>[^/]+)/$',
        SignupView.as_view(), name='invite_signup_form'),
)
