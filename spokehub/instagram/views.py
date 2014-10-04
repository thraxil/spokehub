from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.base import View
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render
from .models import InstagramAccount
from ..main.models import NowPost
from instagram.client import InstagramAPI


class AuthView(View):
    def post(self, request):
        callback_url = ("http://" + request.get_host()
                        + reverse('instagram_callback'))
        unauthenticated_api = InstagramAPI(
            client_id=settings.INSTAGRAM_CLIENT_ID,
            client_secret=settings.INSTAGRAM_CLIENT_SECRET,
            redirect_uri=callback_url)
        url = unauthenticated_api.get_authorize_url()
        return HttpResponseRedirect(url)


class CallbackView(View):
    def get(self, request):
        callback_url = ("http://" + request.get_host()
                        + reverse('instagram_callback'))
        unauthenticated_api = InstagramAPI(
            client_id=settings.INSTAGRAM_CLIENT_ID,
            client_secret=settings.INSTAGRAM_CLIENT_SECRET,
            redirect_uri=callback_url)

        print str(request.GET)
        print str(request.POST)

        code = request.GET.get("code")
        if not code:
            return HttpResponse('Missing code')
        try:
            access_token, user_info = \
                unauthenticated_api.exchange_code_for_access_token(code)
            print "access token: " + access_token
            if not access_token:
                return HttpResponse('Could not get access token')
            InstagramAPI(access_token=access_token)
            print str(user_info)
            ta = InstagramAccount.objects.create(
                user=request.user,
                access_token=access_token,
                screen_name=user_info['username'],
                profile_image_url=user_info['profile_picture'],
                )
            ta.fetch_recent_posts()
            return HttpResponseRedirect(
                '/accounts/' + request.user.username + '/')
        except Exception, e:
            return HttpResponse(e)


class UnlinkView(View):
    def get(self, request):
        if request.user.is_anonymous():
            return HttpResponseRedirect("/")
        ta = InstagramAccount.objects.filter(user=request.user)
        if not ta.exists():
            return HttpResponseRedirect("/")
        return render(request, "instagram/unlink.html", dict())

    def post(self, request):
        if request.user.is_anonymous():
            return HttpResponseRedirect("/")
        ta = InstagramAccount.objects.filter(user=request.user)
        if not ta.exists():
            return HttpResponseRedirect("/")
        NowPost.objects.filter(user=request.user, service="instagram").delete()
        ta.delete()
        return HttpResponseRedirect(
            '/accounts/' + request.user.username + '/')
