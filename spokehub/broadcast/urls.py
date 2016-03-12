from django.conf.urls import patterns, url
from .views import BroadcastView


urlpatterns = patterns(
    '',
    url(r'^$', BroadcastView.as_view(), name='broadcast'),
)
