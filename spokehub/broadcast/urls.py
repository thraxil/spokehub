from django.conf.urls import url
from .views import BroadcastView


urlpatterns = [
    url(r'^$', BroadcastView.as_view(), name='broadcast'),
]
