from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from guardian.decorators import permission_required_or_403

from userena import signals as userena_signals
from userena.decorators import secure_required
from userena.forms import EditProfileForm
from userena.utils import get_profile_model, get_user_profile

import userena.views


USERENA_PROFILE_DETAIL_TEMPLATE = getattr(
    settings, 'USERENA_PROFILE_DETAIL_TEMPLATE',
    'userena/profile_detail.html')


class ProfileListView(userena.views.ProfileListView):
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
                userena_signals.profile_change.send(sender=None,
                                                    user=user)
                redirect_to = success_url
            else:
                redirect_to = reverse('userena_profile_detail',
                                      kwargs={'username': username})
            return redirect(redirect_to)

    if not extra_context:
        extra_context = dict()
    extra_context['form'] = form
    extra_context['profile'] = profile
    return ExtraContextTemplateView.as_view(
        template_name=template_name,
        extra_context=extra_context)(request)
