from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Conversation, NowPost, Reply
from .forms import ReplyUpdateForm, ConversationUpdateForm


class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
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
    fields = ['body']

    def get_success_url(self):
        return reverse('we', args=[])

    def form_valid(self, form):
        convo = form.save(commit=False)
        convo.author = self.request.user
        return super(ConversationCreateView, self).form_valid(form)


class ConversationDetailView(DetailView):
    model = Conversation


class ConversationUpdateView(UpdateView):
    model = Conversation
    form_class = ConversationUpdateForm
    template_name_suffix = '_update_form'


class ConversationDeleteView(DeleteView):
    model = Conversation
    success_url = "/"


class ReplyUpdateView(UpdateView):
    model = Reply
    form_class = ReplyUpdateForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return self.object.item.get_absolute_url()


class ReplyDeleteView(DeleteView):
    model = Reply

    def get_success_url(self):
        return self.object.item.get_absolute_url()


class ReplyToConversationView(View):
    def post(self, request, pk):
        conversation = get_object_or_404(Conversation, pk=pk)
        image = None
        if 'image' in request.FILES:
            image = request.FILES['image']
        conversation.add_reply(
            request.user,
            request.POST.get('body', ''),
            request.POST.get('url', ''),
            image,
        )
        return HttpResponseRedirect(conversation.get_absolute_url())
