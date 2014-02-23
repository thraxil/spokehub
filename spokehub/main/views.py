from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import Item


class IndexView(TemplateView):
    template_name = "main/index.html"


class NewsIndexView(ListView):
    model = Item
    queryset = Item.objects.filter(section='news')
    template_name = "main/news_list.html"


class NewsCreateView(CreateView):
    model = Item

    def get_initial(self):
        return dict(
            section='news',
            author=self.request.user)


class ChallengeIndexView(ListView):
    model = Item
    queryset = Item.objects.filter(section='challenge')
    template_name = "main/challenge_list.html"


class ChallengeCreateView(CreateView):
    model = Item

    def get_initial(self):
        return dict(
            section='challenge',
            author=self.request.user)


class CaseIndexView(ListView):
    model = Item
    queryset = Item.objects.filter(section='case')
    template_name = "main/case_list.html"


class CaseCreateView(CreateView):
    model = Item

    def get_initial(self):
        return dict(
            section='case',
            author=self.request.user)


class ItemDetailView(DetailView):
    model = Item


class ReplyToItemView(View):
    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        item.add_reply(request.user, request.POST.get('body', ''))
        return HttpResponseRedirect(item.get_absolute_url())
