from django.conf.urls import url
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Project


urlpatterns = [
    url(r'^$', ListView.as_view(
        model=Project,
        queryset=Project.objects.filter(published=True),
    ), name='project-list'),
    url(r'(?P<slug>\w+)/$', DetailView.as_view(model=Project),
        name='project-detail'),
]
