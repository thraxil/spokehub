from datetime import datetime
from django.contrib.auth import login
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.urls import reverse
from .models import Invite
from .forms import FullSignupForm
from spokehub.profile.utils import get_user_profile
from spokehub.profile.models import upload_to_mugshot
from userena import settings as userena_settings
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


class InviteTokenRequiredMixin(object):
    def dispatch(self, request, token, *args, **kwargs):
        r = Invite.objects.filter(token=token)
        if not r.exists():
            return HttpResponse("sorry, invalid signup token")
        self.invite = Invite.objects.filter(token=token)[0]
        return super(InviteTokenRequiredMixin,
                     self).dispatch(request, token, *args, **kwargs)


class SignupView(InviteTokenRequiredMixin, FormView):
    template_name = "invite/signup.html"
    form_class = FullSignupForm

    def get_success_url(self):
        return "/accounts/" + self.user.username + "/"

    def get_context_data(self, **kwargs):
        context = super(SignupView, self).get_context_data(**kwargs)
        context['email'] = self.invite.email
        return context

    def form_valid(self, form):
        user = form.save()
        # clear out invite token
        self.invite.delete()

        p = get_user_profile(user)
        self.handle_profile_photo_upload(p)

        # handle cover photo upload
        if 'coverimage' in self.request.FILES:
            p.cover = upload_image('cover', self.request.FILES['coverimage'])

        p.save()

        # log them in
        login(self.request, user,
              backend='django.contrib.auth.backends.ModelBackend')
        self.request.session.set_expiry(
            userena_settings.USERENA_REMEMBER_ME_DAYS[1] * 86400)
        self.user = user
        return super(SignupView, self).form_valid(form)

    def handle_profile_photo_upload(self, p):
        if 'profileimage' in self.request.FILES:
            filename = upload_image('profile',
                                    self.request.FILES['profileimage'])
            if filename is None:
                # they uploaded something that wasn't a photo
                return
            filename = os.path.join(settings.MEDIA_ROOT, filename)
            mugshot_path = upload_to_mugshot(p, filename)
            thumbnailer = get_thumbnailer(
                open(filename, 'rb'), relative_name=mugshot_path)
            thumb = thumbnailer.get_thumbnail(
                {'size': (settings.USERENA_MUGSHOT_SIZE,
                          settings.USERENA_MUGSHOT_SIZE)},
                save=True)
            p.mugshot = thumb.name


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
    except:  # noqa: E722
        pass
    full_filename = path + "%s.%s" % (basename, ext)
    fd = open(settings.MEDIA_ROOT + "/" + full_filename, 'wb')
    for chunk in f.chunks():
        fd.write(chunk)
    fd.close()
    return full_filename
