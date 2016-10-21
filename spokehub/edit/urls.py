from django.conf.urls import url
from django.views.generic import TemplateView
from .views import AddProjectView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="edit/index.html"),
        name='edit-index'),
    url(r'work/add/$', AddProjectView.as_view(), name='add-project'),
]
