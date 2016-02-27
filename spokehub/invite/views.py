from django.contrib.auth import authenticate, login
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import messages
from .models import Invite
from userena.forms import SignupForm
from userena import signals as userena_signals
from userena.utils import get_user_profile
import random
import string


def new_token():
    s = string.ascii_letters + string.digits
    return ''.join([random.choice(s) for x in range(20)])


class InviteView(View):
    template_name = "invite/invite.html"

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        email = request.POST['email']
        token = new_token()
        i = Invite.objects.create(
            email=email, token=token)
        i.send_invite()
        messages.success(request, 'invite sent to ' + email)
        return HttpResponseRedirect(
            reverse("invite_form")
            )


class SignupView(View):
    template_name = "invite/signup.html"

    def get(self, request, token):
        r = Invite.objects.filter(token=token, status='OPEN')
        if not r.exists():
            return HttpResponse("sorry, invalid signup token")
        return render(
            request,
            self.template_name,
            dict(email=r[0].email))

    def post(self, request, token):
        r = Invite.objects.filter(token=token, status='OPEN')
        if not r.exists():
            return HttpResponse("sorry, invalid signup token")

        # do the actual account creation
        form = SignupForm(request.POST, request.FILES)
        if not form.is_valid():
            # TODO handle this properly
            return HttpResponse("missing data")
        user = form.save()
        userena_signals.signup_complete.send(sender=None, user=user)

        # handle profile fields (location, discipline, website, etc)
        p = get_user_profile(user)
        p.website_url = request.POST.get('website', '')
        p.profession = request.POST.get('profession', '')
        p.save()

        # clear out invite token
        r.delete()

        # log them in
        user = authenticate(identification=user.email, check_password=False)
        login(request, user)

        # redirect to profile edit
        return HttpResponseRedirect("/accounts/" + user.username + "/edit/")
