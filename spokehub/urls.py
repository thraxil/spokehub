import os.path
import django.contrib.auth.views
import django.views.static

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic import TemplateView
from spokehub.main import views
from spokehub.profile.forms import ExtendedEditProfileForm
from spokehub.profile.views import (
    ProfileListView, profile_edit, profile_detail,
    password_change, direct_to_user_template, email_confirm,
    email_change,
)
admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__), "../media")

urlpatterns = [
    url(r'^accounts/logout/$',
        django.contrib.auth.views.logout,
        {'next_page': '/'}, name='auth_logout'),
    url(r'^accounts/login/$',
        django.contrib.auth.views.login,
        name='auth_login'),
    url(r'^accounts/(?P<username>[\@\.\w-]+)/edit/$',
        profile_edit,
        {'edit_profile_form': ExtendedEditProfileForm},
        name='profile_edit'),
    url(r'^accounts/(?P<username>(?!(signout|signup|signin)/)[\@\.\+\w-]+)/$',
        profile_detail,
        name='profile_detail'),
    url(r'^accounts/$',
        login_required(ProfileListView.as_view(paginate_by=100)),
        name='profile_list'),
    url(r'^accounts/password/reset/',
        django.contrib.auth.views.password_reset,
        name='password_reset'),
    url(r'^accounts/password/reset/done/',
        django.contrib.auth.views.password_reset_done,
        name='userena_password_reset_done'),
    url(r'^(?P<username>[\@\.\+\w-]+)/password/$',
        password_change,
        name='userena_password_change'),
    url(r'^(?P<username>[\@\.\+\w-]+)/password/complete/$',
        direct_to_user_template,
        {'template_name': 'userena/password_complete.html'},
        name='userena_password_change_complete'),
    url(r'^(?P<username>[\@\.\+\w-]+)/email/$',
        email_change,
        name='userena_email_change'),
    url(r'^(?P<username>[\@\.\+\w-]+)/email/complete/$',
        direct_to_user_template,
        {'template_name': 'userena/email_change_complete.html'},
        name='userena_email_change_complete'),
    url(r'^(?P<username>[\@\.\+\w-]+)/confirm-email/complete/$',
        direct_to_user_template,
        {'template_name': 'userena/email_confirm_complete.html'},
        name='userena_email_confirm_complete'),
    url(r'^confirm-email/(?P<confirmation_key>\w+)/$',
        email_confirm,
        name='userena_email_confirm'),
    url(r'^accounts/', include('django.contrib.auth.urls')),

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^about/$', TemplateView.as_view(template_name="about.html"),
        name='about'),
    url(r'^network/$', views.IndexView.as_view(
        template_name='network/index.html')),
    url(r'^how/$', views.IndexView.as_view(
        template_name='how/index.html'), name='how'),

    url(r'^we/$', views.ConversationIndexView.as_view(
        template_name='we/index.html'), name='we'),
    url(r'^we/archive/$', views.ConversationIndexView.as_view(
        paginate_by=10, template_name='we/archive.html'),
        name='we-archive'),
    url(r'^we/question/(?P<year>\d+)/'
        '(?P<month>\d+)/(?P<day>\d+)/(?P<pk>\d+)/$',
        views.ConversationDetailView.as_view(
            template_name='we/question.html'), name='question'),
    url(r'^we/question/(?P<year>\d+)/(?P<month>\d+)/'
        r'(?P<day>\d+)/(?P<pk>\d+)/edit/$',
        views.ConversationUpdateView.as_view(), name='edit-question'),
    url(r'^we/question/(?P<year>\d+)/(?P<month>\d+)/'
        r'(?P<day>\d+)/(?P<pk>\d+)/delete/$',
        views.ConversationDeleteView.as_view(), name='delete-question'),
    url(r'^we/ask/$', views.ConversationCreateView.as_view(
        template_name='we/ask.html'), name='ask-question'),
    url(r'^reply/(?P<pk>\d+)/edit/$',
        views.ReplyUpdateView.as_view(), name='edit-reply'),
    url(r'^reply/(?P<pk>\d+)/delete/$',
        views.ReplyDeleteView.as_view(), name='delete-reply'),
    url(r'^reply/(?P<pk>\d+)/add_comment/$',
        views.AddCommentView.as_view(), name='add-comment'),

    url(r'^work/', include('spokehub.work.urls')),

    url(r'^now/$', views.IndexView.as_view(
        template_name='now/index.html'), name='now'),
    url(r'^weold/$', views.IndexView.as_view(
        template_name='main/we.html')),
    url(r'^convo/$', views.IndexView.as_view(
        template_name='main/conversation.html')),
    url(r'^404-test/$', views.IndexView.as_view(
        template_name='404.html')),
    url(r'^user_index/$', views.TemplateView.as_view(
        template_name='userena/user_index.html')),
    url(r'^privacy/$', views.TemplateView.as_view(
        template_name='main/privacy.html')),

    url(r'^scroll/$', views.TemplateView.as_view(
        template_name='infinite-scroll-master/test/index.html'),
        name='scroll'),

    url(r'^conversation/(?P<pk>\d+)/reply/$',
        views.ReplyToConversationView.as_view(),
        name='reply-to-question'),

    url(r'^test/$', TemplateView.as_view(template_name='layout_test.html')),

    url(r'^edit/', include('spokehub.edit.urls')),
    url(r'^invite/', include('spokehub.invite.urls')),
    url(r'^contact/', include('spokehub.contact.urls')),
    url(r'^broadcast/', include('spokehub.broadcast.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^stats/$', TemplateView.as_view(template_name="stats.html"),
        name='stats'),
    url(r'^smoketest/', include('smoketest.urls')),
    url(r'^uploads/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT}),
]
