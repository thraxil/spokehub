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

    url(r'^accounts/signout/(?P<next_page>.*)/$',
        'userena.views.signout', name='userena_signout_next'),
    (r'^accounts/', include('userena.urls')),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^about/$', TemplateView.as_view(template_name="about.html"),
        name='about'),
    (r'^network/$', views.IndexView.as_view(
        template_name='network/index.html')),
    (r'^contact/$', views.IndexView.as_view(
        template_name='contact/index.html')),
    url(r'^how/$', views.IndexView.as_view(
        template_name='how/index.html'), name='how'),

    url(r'^salvattore/$', views.IndexView.as_view(
        template_name='salvattore/salvattore.html'), name='how'),

    url(r'^we/$', views.ConversationIndexView.as_view(
        template_name='we/index.html'), name='we'),
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

    url(r'^work/$', views.TemplateView.as_view(
        template_name='work/index.html'), name='work'),
    url(r'^work/maddie/$', views.TemplateView.as_view(
        template_name='work/maddie/index.html'), name='work-maddie'),
    url(r'^work/havana/$', views.TemplateView.as_view(
        template_name='work/havana/index.html'), name='work-havana'),
    url(r'^work/fightclub/$', views.TemplateView.as_view(
        template_name='work/fightclub/index.html'), name='work-fightclub'),
    url(r'^work/sperry/$', views.TemplateView.as_view(
        template_name='work/sperry/index.html'), name='work-sperry'),
    url(r'^work/supper/$', views.TemplateView.as_view(
        template_name='work/supper/index.html'), name='work-supper'),
    url(r'^work/artsho5/$', views.TemplateView.as_view(
        template_name='work/artsho5/index.html'), name='work-artsho5'),
    url(r'^work/sorry/$', views.TemplateView.as_view(
        template_name='work/sorry/index.html'), name='work-sorry'),
    url(r'^work/bca/$', views.TemplateView.as_view(
        template_name='work/bca/index.html'), name='work-bca'),

    url(r'^now/$', views.IndexView.as_view(
        template_name='now/index.html'), name='now'),
    (r'^weold/$', views.IndexView.as_view(
        template_name='main/we.html')),
    (r'^convo/$', views.IndexView.as_view(
        template_name='main/conversation.html')),

    url(r'^conversation/(?P<pk>\d+)/reply/$',
        views.ReplyToConversationView.as_view(),
        name='reply-to-question'),

    (r'^test/$', TemplateView.as_view(template_name='layout_test.html')),

    (r'^invite/', include('spokehub.invite.urls')),
    (r'^admin/', include(admin.site.urls)),
    url(r'^_impersonate/', include('impersonate.urls')),
    url(r'^stats/$', TemplateView.as_view(template_name="stats.html"),
        name='stats'),
    (r'^smoketest/', include('smoketest.urls')),
    (r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
)
