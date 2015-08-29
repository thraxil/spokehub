from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Conversation, NowPost


class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['team'] = User.objects.all().exclude(username='AnonymousUser')
        context['conversations'] = Conversation.objects.newest()

        now_posts_list = NowPost.objects.newest()
        paginator = Paginator(now_posts_list, 50)
        page = self.request.GET.get('page')
        try:
            now_posts = paginator.page(page)
        except PageNotAnInteger:
            now_posts = paginator.page(1)
        except EmptyPage:
            now_posts = paginator.page(paginator.num_pages)
        context['now_posts'] = now_posts
        return context


class ConversationIndexView(ListView):
    model = Conversation
    queryset = Conversation.objects.filter()
    template_name = "main/conversation_list.html"


class ConversationCreateView(CreateView):
    model = Conversation
    fields = ['title', 'body']

    success_url = "/#we"

    def get_initial(self):
        return dict(author=self.request.user)


class ConversationDetailView(DetailView):
    model = Conversation


class ConversationUpdateView(UpdateView):
    model = Conversation
    fields = ['title', 'body']
    template_name_suffix = '_update_form'


class ConversationDeleteView(DeleteView):
    model = Conversation
    success_url = "/"


class ReplyToConversationView(View):
    def post(self, request, pk):
        conversation = get_object_or_404(Conversation, pk=pk)
        reply = conversation.add_reply(
            request.user,
            request.POST.get('body', ''),
            request.POST.get('url', ''),
            request.POST.get('title', ''))
        if 'image' in request.FILES:
            reply.save_image(request.FILES['image'])

        reply.email_mentions()
        reply.body = reply.link_usernames()
        reply.save()
        return HttpResponseRedirect('/#we')
