from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.conf import settings
from django.core.urlresolvers import reverse
from .models import TwitterAccount
import tweepy


class AuthView(View):
    def post(self, request):
        callback_url = ("http://" + request.get_host()
                        + reverse('twitter_callback'))
        auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY,
                                   settings.TWITTER_API_SECRET,
                                   callback_url)
        return HttpResponseRedirect(auth.get_authorization_url())


class CallbackView(View):
    def get(self, request):
        TwitterAccount.objects.create(
            user=request.user,
            oauth_token=request.GET.get('oauth_token'),
            oauth_verifier=request.GET.get('oauth_verifier'))
        return HttpResponseRedirect(
            '/accounts/' + request.user.username + '/')
