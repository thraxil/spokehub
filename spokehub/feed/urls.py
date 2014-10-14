from django.conf.urls import patterns, url
from .views import AddView, UnlinkView

urlpatterns = patterns(
    '',
    url(r'^add/$', AddView.as_view(), name='feed_add'),
    url(r'^unlink/$', UnlinkView.as_view()),
)
