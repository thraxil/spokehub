from django.conf.urls import url
from .views import InviteView, SignupView


urlpatterns = [
    url(r'^$', InviteView.as_view(), name='invite_form'),
    url(r'^signup/(?P<token>[^/]+)/$',
        SignupView.as_view(), name='invite_signup_form'),
]
