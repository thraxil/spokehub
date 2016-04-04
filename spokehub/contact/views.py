from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView


from .forms import ContactForm


class ContactView(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactForm
    success_url = '/'

    def form_valid(self, form):
        form.send_email()
        return super(ContactView, self).form_valid(form)

    def get_success_url(self):
        return reverse('contact_thanks')


class ThanksView(TemplateView):
    template_name = 'contact/thanks.html'
