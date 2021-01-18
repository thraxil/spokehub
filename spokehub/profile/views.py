from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import PermissionDenied
from django.dispatch import Signal
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.functional import wraps
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from guardian.decorators import permission_required_or_403

from .forms import EditProfileForm, ChangeEmailForm
from .models import UserenaSignup
from .utils import get_profile_model, get_user_profile


USERENA_PROFILE_DETAIL_TEMPLATE = getattr(
    settings, 'USERENA_PROFILE_DETAIL_TEMPLATE',
    'userena/profile_detail.html')
USERENA_PROFILE_LIST_TEMPLATE = getattr(
    settings, 'USERENA_PROFILE_LIST_TEMPLATE',
    'userena/profile_list.html')
USERENA_WITHOUT_USERNAMES = getattr(
    settings,
    'USERENA_WITHOUT_USERNAMES',
    False)
DEFAULT_USERENA_USE_HTTPS = False
password_complete = Signal(providing_args=["user", ])
profile_change = Signal(providing_args=["user", ])


def secure_required(view_func):
    """
    Decorator to switch an url from http to https.
    If a view is accessed through http and this decorator is applied to that
    view, than it will return a permanent redirect to the secure (https)
    version of the same view.
    The decorator also must check that ``USERENA_USE_HTTPS`` is enabled. If
    disabled, it should not redirect to https because the project doesn't
    support it.
    """
    def _wrapped_view(request, *args, **kwargs):
        if not request.is_secure():
            if getattr(settings, 'USERENA_USE_HTTPS',
                       DEFAULT_USERENA_USE_HTTPS):
                request_url = request.build_absolute_uri(
                    request.get_full_path())
                secure_url = request_url.replace('http://', 'https://')
                return HttpResponsePermanentRedirect(secure_url)
        return view_func(request, *args, **kwargs)
    return wraps(view_func)(_wrapped_view)


class ProfileListView(ListView):
    """ Lists all profiles """
    context_object_name = 'profile_list'
    page = 1
    paginate_by = 50
    template_name = USERENA_PROFILE_LIST_TEMPLATE
    extra_context = None

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProfileListView, self).get_context_data(**kwargs)
        try:
            page = int(self.request.GET.get('page', None))
        except (TypeError, ValueError):
            page = self.page

        if not self.extra_context:
            self.extra_context = dict()

        context['page'] = page
        context['paginate_by'] = self.paginate_by
        context['extra_context'] = self.extra_context

        return context

    def get_queryset(self):
        profile_model = get_profile_model()
        queryset = profile_model.objects.get_visible_profiles(
            self.request.user).order_by('user__username').select_related()
        return queryset


# imported directly from djangp-userena
class ExtraContextTemplateView(TemplateView):
    """ Add extra context to a simple template view """
    extra_context = None

    def get_context_data(self, *args, **kwargs):
        context = super(ExtraContextTemplateView, self).get_context_data(
            *args, **kwargs)
        if self.extra_context:
            context.update(self.extra_context)
        return context

    post = TemplateView.get


def profile_detail(request, username,
                   template_name=USERENA_PROFILE_DETAIL_TEMPLATE,
                   extra_context=None, **kwargs):
    user = get_object_or_404(get_user_model(), username__iexact=username)
    profile = get_user_profile(user=user)
    if not profile.can_view_profile(request.user):
        raise PermissionDenied
    if not extra_context:
        extra_context = dict()
    extra_context['profile'] = profile
    return ExtraContextTemplateView.as_view(
        template_name=template_name,
        extra_context=extra_context)(request)


@secure_required
@permission_required_or_403('change_profile',
                            (get_profile_model(),
                             'user__username', 'username'))
def profile_edit(request, username, edit_profile_form=EditProfileForm,
                 template_name='userena/profile_form.html', success_url=None,
                 extra_context=None, **kwargs):
    user = get_object_or_404(get_user_model(), username__iexact=username)

    profile = get_user_profile(user=user)

    user_initial = {'first_name': user.first_name,
                    'last_name': user.last_name}

    form = edit_profile_form(instance=profile, initial=user_initial)

    if request.method == 'POST':
        form = edit_profile_form(request.POST, request.FILES, instance=profile,
                                 initial=user_initial)

        if form.is_valid():
            profile = form.save()

            messages.success(request, _('Your profile has been updated.'),
                             fail_silently=True)

            if success_url:
                # Send a signal that the profile has changed
                profile_change.send(sender=None, user=user)
                redirect_to = success_url
            else:
                redirect_to = reverse('profile_detail',
                                      kwargs={'username': username})
            return redirect(redirect_to)

    if not extra_context:
        extra_context = dict()
    extra_context['form'] = form
    extra_context['profile'] = profile
    return ExtraContextTemplateView.as_view(
        template_name=template_name,
        extra_context=extra_context)(request)


@secure_required
@permission_required_or_403('change_user',
                            (get_user_model(), 'username', 'username'))
def password_change(request, username,
                    template_name='userena/password_form.html',
                    pass_form=PasswordChangeForm, success_url=None,
                    extra_context=None):
    user = get_object_or_404(get_user_model(),
                             username__iexact=username)

    form = pass_form(user=user)

    if request.method == "POST":
        form = pass_form(user=user, data=request.POST)
        if form.is_valid():
            form.save()

            # Send a signal that the password has changed
            password_complete.send(sender=None, user=user)

            if success_url:
                redirect_to = success_url
            else:
                redirect_to = reverse('password_change_complete',
                                      kwargs={'username': user.username})
            return redirect(redirect_to)

    if not extra_context:
        extra_context = dict()
    extra_context['form'] = form
    extra_context['profile'] = get_user_profile(user=user)
    return ExtraContextTemplateView.as_view(
        template_name=template_name,
        extra_context=extra_context)(request)


def direct_to_user_template(request, username, template_name,
                            extra_context=None):
    user = get_object_or_404(get_user_model(), username__iexact=username)

    if not extra_context:
        extra_context = dict()
    extra_context['viewed_user'] = user
    extra_context['profile'] = get_user_profile(user=user)
    return ExtraContextTemplateView.as_view(
        template_name=template_name,
        extra_context=extra_context)(request)


@secure_required
@permission_required_or_403('change_user',
                            (get_user_model(), 'username', 'username'))
def email_change(request, username, email_form=ChangeEmailForm,
                 template_name='userena/email_form.html', success_url=None,
                 extra_context=None):
    user = get_object_or_404(get_user_model(), username__iexact=username)
    prev_email = user.email
    form = email_form(user)

    if request.method == 'POST':
        form = email_form(user, request.POST, request.FILES)

        if form.is_valid():
            form.save()

            if success_url:
                # Send a signal that the email has changed
                email_change.send(sender=None,
                                  user=user,
                                  prev_email=prev_email,
                                  new_email=user.email)
                redirect_to = success_url
            else:
                redirect_to = reverse('userena_email_change_complete',
                                      kwargs={'username': user.username})
            return redirect(redirect_to)

    if not extra_context:
        extra_context = dict()
    extra_context['form'] = form
    extra_context['profile'] = get_user_profile(user=user)
    return ExtraContextTemplateView.as_view(
        template_name=template_name,
        extra_context=extra_context)(request)


@secure_required
def email_confirm(request, confirmation_key,
                  template_name='userena/email_confirm_fail.html',
                  success_url=None, extra_context=None):
    user = UserenaSignup.objects.confirm_email(confirmation_key)
    if user:
        messages.success(request, _('Your email address has been changed.'),
                         fail_silently=True)

        if success_url:
            redirect_to = success_url
        else:
            redirect_to = reverse('userena_email_confirm_complete',
                                  kwargs={'username': user.username})
        return redirect(redirect_to)
    else:
        if not extra_context:
            extra_context = dict()
        return ExtraContextTemplateView.as_view(
            template_name=template_name,
            extra_context=extra_context)(request)
