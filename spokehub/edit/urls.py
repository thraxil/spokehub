from django.conf.urls import url
from django.contrib.admin.views.decorators import (
    staff_member_required as staff)
from .views import (
    IndexView, AddProjectView, ProjectUpdate, ProjectDelete,
    ProjectAddContributor, ProjectContributorDelete,
    ProjectPublish, ProjectDraft, ProjectAddMedia,
    ProjectMediaDelete, ReorderProjectMedia, ReorderProjectContributors,
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
    url(r'work/(?P<pk>\d+)/add_media/$',
        staff(ProjectAddMedia.as_view()), name='add-media'),
    url(r'work/(?P<pk>\d+)/publish/$', staff(ProjectPublish.as_view()),
        name='publish-project'),
    url(r'work/(?P<pk>\d+)/draft/$', staff(ProjectDraft.as_view()),
        name='draft-project'),
    url(r'work/(?P<pk>\d+)/reorder_media/$',
        staff(ReorderProjectMedia.as_view()), name='reorder-project-media'),
    url(r'work/(?P<pk>\d+)/reorder_contributors/$',
        staff(ReorderProjectContributors.as_view()),
        name='reorder-project-contributors'),
    url(r'contributor/(?P<pk>\d+)/delete/$',
        staff(ProjectContributorDelete.as_view()), name='remove-contributor'),
    url(r'media/(?P<pk>\d+)/delete/$', staff(ProjectMediaDelete.as_view()),
        name='remove-media'),
]
