from django.conf.urls import url
from .views import (
    IndexView, AddProjectView, ProjectUpdate, ProjectDelete)


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='edit-index'),
    url(r'work/add/$', AddProjectView.as_view(), name='add-project'),
    url(r'work/(?P<pk>\d+)/$', ProjectUpdate.as_view(), name='edit-project'),
    url(r'work/(?P<pk>\d+)/delete/$', ProjectDelete.as_view(),
        name='delete-project'),
]