from django.conf.urls import url
from .views import ContactView, ThanksView


urlpatterns = [
    url(r'^$', ContactView.as_view(), name='contact_form'),
    url(r'^thanks/$', ThanksView.as_view(), name='contact_thanks'),
]
