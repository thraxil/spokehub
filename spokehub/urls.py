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
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^about/$', TemplateView.as_view(template_name="about.html"),
        name='about'),
    url(r'^conversation/$', views.ConversationIndexView.as_view(), {},
        'conversation-index'),
    url((r'^conversation/(?P<year>\d+)/'
         '(?P<month>\d+)/(?P<day>\d+)/(?P<pk>\d+)/$'),
        views.ConversationDetailView.as_view(), {}, 'conversation'),
    url(r'^conversation/(?P<year>\d+)/(?P<month>\d+)/'
        r'(?P<day>\d+)/(?P<pk>\d+)/edit/$',
        views.ConversationUpdateView.as_view(), name='edit-conversation'),
    url(r'^conversation/(?P<year>\d+)/(?P<month>\d+)/'
        r'(?P<day>\d+)/(?P<pk>\d+)/delete/$',
        views.ConversationDeleteView.as_view(), name='delete-conversation'),
    url(r'^conversation/add/$', views.ConversationCreateView.as_view(),
        name='add-conversation'),
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
    (r'^we/questionold/$', views.IndexView.as_view(
        template_name='we/question-old.html')),
    (r'^we/ask/$', views.IndexView.as_view(
        template_name='we/ask.html')),

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

    (r'^now/$', views.IndexView.as_view(
        template_name='now/index.html')),
    (r'^weold/$', views.IndexView.as_view(
        template_name='main/we.html')),
    (r'^convo/$', views.IndexView.as_view(
        template_name='main/conversation.html')),

    (r'^signupform/$', views.IndexView.as_view(
        template_name='userarena/signup_form.html')),

    (r'^profilecompletion/$',
     TemplateView.as_view(template_name='profile-completion.html')),

    url(r'^conversation/(?P<pk>\d+)/reply/$',
        views.ReplyToConversationView.as_view(),
        name='reply-to-conversation'),

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
