from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.shortcuts import render
from .models import UserFeed
from ..main.models import NowPost


class AddView(View):
    def post(self, request):
        if request.user.is_anonymous():
            return HttpResponseRedirect("/")
        url = request.POST.get('feed_url', '')
        UserFeed.objects.create(user=request.user, url=url)
        return HttpResponseRedirect('/accounts/' + request.user.username)


class UnlinkView(View):
    def get(self, request):
        if request.user.is_anonymous():
            return HttpResponseRedirect("/")
        ta = UserFeed.objects.filter(user=request.user)
        if not ta.exists():
            return HttpResponseRedirect("/")
        return render(request, "feed/unlink.html", dict())

    def post(self, request):
        if request.user.is_anonymous():
            return HttpResponseRedirect("/")
        ta = UserFeed.objects.filter(user=request.user)
        if not ta.exists():
            return HttpResponseRedirect("/")
        NowPost.objects.filter(user=request.user, service="feed").delete()
        ta.delete()
        return HttpResponseRedirect(
            '/accounts/' + request.user.username + '/')
