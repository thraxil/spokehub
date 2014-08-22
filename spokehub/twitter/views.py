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
        url = auth.get_authorization_url()
        request.session[
            'twitter_request_token_key'] = auth.request_token.key
        request.session[
            'twitter_request_token_secret'] = auth.request_token.secret
        return HttpResponseRedirect(url)


class CallbackView(View):
    def get(self, request):
        auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY,
                                   settings.TWITTER_API_SECRET)
        auth.set_request_token(
            request.session['twitter_request_token_key'],
            request.session['twitter_request_token_secret']
            )
        verifier = request.GET.get('oauth_verifier')
        auth.get_access_token(verifier)
        ta = TwitterAccount.objects.create(
            user=request.user,
            oauth_token=auth.access_token.key,
            oauth_verifier=auth.access_token.secret)
        ta.update_details()
        return HttpResponseRedirect(
            '/accounts/' + request.user.username + '/')
