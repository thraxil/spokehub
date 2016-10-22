from django.conf.urls import url
from django.contrib.admin.views.decorators import (
    staff_member_required as staff)
from .views import (
    IndexView, AddProjectView, ProjectUpdate, ProjectDelete,
    ProjectAddContributor, ProjectContributorDelete,
)


urlpatterns = [
    url(r'^$', staff(IndexView.as_view()), name='edit-index'),
    url(r'work/add/$', staff(AddProjectView.as_view()), name='add-project'),
    url(r'work/(?P<pk>\d+)/$', staff(ProjectUpdate.as_view()),
        name='edit-project'),
    url(r'work/(?P<pk>\d+)/delete/$', staff(ProjectDelete.as_view()),
        name='delete-project'),
    url(r'work/(?P<pk>\d+)/add_contributor/$',
        staff(ProjectAddContributor.as_view()), name='add-contributor'),
    url(r'contributor/(?P<pk>\d+)/delete/$',
        staff(ProjectContributorDelete.as_view()), name='remove-contributor'),
]
