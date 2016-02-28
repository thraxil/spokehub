from datetime import datetime
from django.contrib.auth import authenticate, login
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import messages
from django.template.defaultfilters import slugify
from .models import Invite
from userena.forms import SignupForm
from userena import signals as userena_signals
from userena.utils import get_user_profile
from userena.models import upload_to_mugshot
from easy_thumbnails.files import get_thumbnailer
import random
import string
import os


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

        user.first_name = request.POST['firstname']
        user.last_name = request.POST['lastname']
        user.save()

        # handle profile fields (location, discipline, website, etc)
        p = get_user_profile(user)
        p.website_url = request.POST.get('website', '')
        p.website_name = request.POST.get('websitename', '')
        p.profession = request.POST.get('profession', '')
        p.location = request.POST.get('location', '')

        # handle profile photo upload
        if 'profileimage' in request.FILES:
            filename = upload_image('profile', request.FILES['profileimage'])
            filename = os.path.join(settings.MEDIA_ROOT, filename)
            mugshot_path = upload_to_mugshot(p, filename)
            thumbnailer = get_thumbnailer(
                open(filename, 'rb'), relative_name=mugshot_path)
            thumb = thumbnailer.get_thumbnail(
                {'size': (settings.USERENA_MUGSHOT_SIZE,
                          settings.USERENA_MUGSHOT_SIZE)},
                save=True)
            p.mugshot = thumb.name

        # handle cover photo upload
        if 'coverimage' in request.FILES:
            p.cover = upload_image('cover', request.FILES['coverimage'])

        p.save()

        # clear out invite token
        r.delete()

        # log them in
        user = authenticate(identification=user.email, check_password=False)
        login(request, user)

        # redirect to profile edit
        return HttpResponseRedirect("/accounts/" + user.username + "/edit/")


def upload_image(d, f):
    ext = f.name.split(".")[-1].lower()
    basename = slugify(f.name.split(".")[-2].lower())[:20]
    if ext not in ['jpg', 'jpeg', 'gif', 'png']:
        # unsupported image format
        return None
    now = datetime.now()
    path = "%simages/%04d/%02d/%02d/" % (d, now.year, now.month, now.day)
    try:
        os.makedirs(settings.MEDIA_ROOT + "/" + path)
    except:
        pass
    full_filename = path + "%s.%s" % (basename, ext)
    fd = open(settings.MEDIA_ROOT + "/" + full_filename, 'wb')
    for chunk in f.chunks():
        fd.write(chunk)
    fd.close()
    return full_filename
