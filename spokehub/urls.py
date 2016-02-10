from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from spokehub.main import views
import os.path
admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__), "../media")

urlpatterns = patterns(
    '',

    (r'^accounts/', include('userena.urls')),
    (r'^$', views.IndexView.as_view()),

    (r'^about/$', TemplateView.as_view(template_name="about.html")),

    url(r'^conversation/$', views.ConversationIndexView.as_view(), {},
        'conversation-index'),
    url((r'^conversation/(?P<year>\d+)/'
         '(?P<month>\d+)/(?P<day>\d+)/(?P<pk>\d+)/$'),
        views.ConversationDetailView.as_view(), {}, 'conversation'),
    (r'^conversation/(?P<year>\d+)/(?P<month>\d+)/'
     r'(?P<day>\d+)/(?P<pk>\d+)/edit/$',
     views.ConversationUpdateView.as_view()),
    (r'^conversation/(?P<year>\d+)/(?P<month>\d+)/'
     r'(?P<day>\d+)/(?P<pk>\d+)/delete/$',
     views.ConversationDeleteView.as_view()),
    (r'^conversation/add/$', views.ConversationCreateView.as_view()),

    (r'^network/$', views.IndexView.as_view(
        template_name='network/index.html')),
    (r'^contact/$', views.IndexView.as_view(
        template_name='contact/index.html')),
    (r'^how/$', views.IndexView.as_view(
        template_name='how/index.html')),
    (r'^we/$', views.IndexView.as_view(
        template_name='we/index.html')),
    (r'^we/question/$', views.IndexView.as_view(
        template_name='we/question.html')),
    (r'^work/$', views.IndexView.as_view(
        template_name='work/index.html')),
    (r'^work/maddie/$', views.IndexView.as_view(
        template_name='work/maddie/index.html')),
    (r'^work/havana/$', views.IndexView.as_view(
        template_name='work/havana/index.html')),
    (r'^work/fightclub/$', views.IndexView.as_view(
        template_name='work/fightclub/index.html')),
    (r'^work/sperry/$', views.IndexView.as_view(
        template_name='work/sperry/index.html')),
    (r'^work/supper/$', views.IndexView.as_view(
        template_name='work/supper/index.html')),
    (r'^work/artsho5/$', views.IndexView.as_view(
        template_name='work/artsho5/index.html')),
    (r'^work/sorry/$', views.IndexView.as_view(
        template_name='work/sorry/index.html')),
    (r'^work/bca/$', views.IndexView.as_view(
        template_name='work/bca/index.html')),
    (r'^now/$', views.IndexView.as_view(
        template_name='now/index.html')),

    (r'^profilecompletion/$',
     TemplateView.as_view(template_name='profile-completion.html')),

    (r'^conversation/(?P<pk>\d+)/reply/$',
     views.ReplyToConversationView.as_view()),

    (r'^test/$', TemplateView.as_view(template_name='layout_test.html')),

    (r'^invite/', include('spokehub.invite.urls')),
    (r'^admin/', include(admin.site.urls)),
    url(r'^_impersonate/', include('impersonate.urls')),
    (r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    (r'^smoketest/', include('smoketest.urls')),
    (r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
)
