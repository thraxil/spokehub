from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import messages
from .models import Invite
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
