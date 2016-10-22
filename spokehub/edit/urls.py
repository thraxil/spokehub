from django.conf.urls import url
from .views import IndexView, AddProjectView


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='edit-index'),
    url(r'work/add/$', AddProjectView.as_view(), name='add-project'),
]
