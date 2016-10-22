from django.conf.urls import url
from django.views.generic.detail import DetailView

from .models import Project


urlpatterns = [
    url(r'(?P<slug>\w+)/$', DetailView.as_view(model=Project),
        name='project-detail'),
]
