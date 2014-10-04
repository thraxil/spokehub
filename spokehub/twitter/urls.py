from django.conf.urls import patterns, url
from .views import AuthView, CallbackView, UnlinkView

urlpatterns = patterns(
    '',
    url(r'^auth/$', AuthView.as_view(), name='twitter_auth'),
    url(r'^callback/$', CallbackView.as_view(),
        name='twitter_callback'),
    url(r'^unlink/$', UnlinkView.as_view()),
)
