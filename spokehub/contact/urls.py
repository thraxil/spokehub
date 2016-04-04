from django.conf.urls import patterns, url
from .views import ContactView, ThanksView


urlpatterns = patterns(
    '',
    url(r'^$', ContactView.as_view(), name='contact_form'),
    url(r'^thanks/$', ThanksView.as_view(), name='contact_thanks'),
)
