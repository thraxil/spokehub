from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Item, WorkSample, NowPost
import random


class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['team'] = User.objects.all().exclude(username='AnonymousUser')
        work_samples = list(WorkSample.objects.all())
        random.shuffle(work_samples)
        context['work_samples'] = work_samples
        if Item.objects.all().count() > 0:
            context['conversation'] = Item.objects.all()[0]

        now_posts_list = NowPost.objects.all().order_by("-created")
        paginator = Paginator(now_posts_list, 100)
        page = self.request.GET.get('page')
        try:
            now_posts = paginator.page(page)
        except PageNotAnInteger:
            now_posts = paginator.page(1)
        except EmptyPage:
            now_posts = paginator.page(paginator.num_pages)
        context['now_posts'] = now_posts
        return context


class ItemIndexView(ListView):
    model = Item
    queryset = Item.objects.filter()
    template_name = "main/item_list.html"


class ItemCreateView(CreateView):
    model = Item
    fields = ['title', 'body']

    def get_initial(self):
        return dict(author=self.request.user)


class ItemDetailView(DetailView):
    model = Item


class ItemUpdateView(UpdateView):
    model = Item
    fields = ['title', 'body']
    template_name_suffix = '_update_form'


class ItemDeleteView(DeleteView):
    model = Item
    success_url = "/"


class ReplyToItemView(View):
    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        reply = item.add_reply(
            request.user,
            request.POST.get('body', ''),
            request.POST.get('url', ''),
            request.POST.get('title', ''))
        if 'image' in request.FILES:
            reply.save_image(request.FILES['image'])

        if 'item' in request.META.get('HTTP_REFERER'):
            return HttpResponseRedirect(item.get_absolute_url())
        else:
            return HttpResponseRedirect('/')


class AddWorkSampleView(View):
    def post(self, request):
        title = request.POST.get('title', 'no title')
        ws = WorkSample.objects.create(title=title, user=request.user)
        ws.save_image(request.FILES['image'])
        ws.save()
        return HttpResponseRedirect("/accounts/%s/" % request.user.username)


class DeleteWorkSampleView(DeleteView):
    model = WorkSample

    def get_success_url(self):
        return "/accounts/" + self.object.user.username + "/"
