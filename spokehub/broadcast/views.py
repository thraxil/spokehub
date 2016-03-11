from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from .forms import BroadcastForm


class BroadcastView(FormView):
    template_name = "broadcast/broadcast.html"
    form_class = BroadcastForm
    success_url = "/"

    def form_valid(self, form):
        for u in User.objects.all().exclude(username='AnonymousUser'):
            u.email_user(
                form.cleaned_data['subject'],
                form.cleaned_data['body'],
                'Hub Conversation <hello@spokehub.org>',
            )
        return super(BroadcastView, self).form_valid(form)
