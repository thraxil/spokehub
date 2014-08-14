from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView
from .models import Item, WorkSample


class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['team'] = User.objects.all().exclude(username='AnonymousUser')
        context['work_samples'] = WorkSample.objects.all()
        if Item.objects.all().count() > 0:
            context['conversation'] = Item.objects.all()[0]
        return context


class ItemIndexView(ListView):
    model = Item
    queryset = Item.objects.filter()
    template_name = "main/item_list.html"


class ItemCreateView(CreateView):
    model = Item

    def get_initial(self):
        return dict(author=self.request.user)


class ItemDetailView(DetailView):
    model = Item


class ReplyToItemView(View):
    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        item.add_reply(request.user, request.POST.get('body', ''))
        return HttpResponseRedirect(item.get_absolute_url())


class AddWorkSampleView(View):
    def post(self, request):
        title = request.POST.get('title', 'no title')
        caption = request.POST.get('caption', '')
        ws = WorkSample.objects.create(title=title, user=request.user,
                                       caption=caption)
        ws.save_image(request.FILES['image'])
        ws.save()
        return HttpResponseRedirect("/accounts/%s/" % request.user.username)


class DeleteWorkSampleView(DeleteView):
    model = WorkSample

    def get_success_url(self):
        return "/accounts/" + self.object.user.username + "/"
