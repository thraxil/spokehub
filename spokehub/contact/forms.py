from django import forms
from django.core.mail import send_mail


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']

        send_mail(
            'New Contact Message',
            """New message from: %s <%s>

%s
            """ % (name, email, message),
            'Hub Contact <hello@spokehub.org>',
            ['hello@spokehub.org'],
            fail_silently=False,
        )
