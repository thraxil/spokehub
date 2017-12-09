from collections import OrderedDict
from django import forms
from django.contrib.auth import get_user_model
from django.forms import CharField
from django.utils.translation import ugettext_lazy as _
from .utils import get_profile_model


class EditProfileForm(forms.ModelForm):
    """ Base form used for fields that are always required """
    first_name = forms.CharField(label=_('First name'),
                                 max_length=30,
                                 required=False)
    last_name = forms.CharField(label=_('Last name'),
                                max_length=30,
                                required=False)

    def __init__(self, *args, **kw):
        super(EditProfileForm, self).__init__(*args, **kw)
        # Put the first and last name at the top
        try:  # in Django < 1.7
            new_order = self.fields.keyOrder[:-2]
            new_order.insert(0, 'first_name')
            new_order.insert(1, 'last_name')
            self.fields.keyOrder = new_order
        except AttributeError:  # in Django > 1.7
            new_order = [('first_name', self.fields['first_name']),
                         ('last_name', self.fields['last_name'])]
            new_order.extend(list(self.fields.items())[:-2])
            self.fields = OrderedDict(new_order)

    class Meta:
        model = get_profile_model()
        exclude = ['user']

    def save(self, force_insert=False, force_update=False, commit=True):
        profile = super(EditProfileForm, self).save(commit=commit)
        # Save first and last name
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        return profile


class ExtendedEditProfileForm(EditProfileForm):
    first_name = CharField(label='First name', max_length=30, required=True)
    last_name = CharField(label='Last name', max_length=30, required=True)

    def clean_website_url(self):
        if self.cleaned_data['website_url'].startswith('https://'):
            return self.cleaned_data['website_url']
        elif self.cleaned_data['website_url'].startswith('http://'):
            return self.cleaned_data['website_url']
        else:
            return 'http://' + self.cleaned_data['website_url']


attrs_dict = {'class': 'required'}


class ChangeEmailForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_("New email"))

    def __init__(self, user, *args, **kwargs):
        super(ChangeEmailForm, self).__init__(*args, **kwargs)
        if not isinstance(user, get_user_model()):
            raise TypeError(
                "user must be an instance of %s" % get_user_model().__name__)
        else:
            self.user = user

    def clean_email(self):
        if self.cleaned_data['email'].lower() == self.user.email:
            raise forms.ValidationError(
                _('You\'re already known under this email.'))
        if get_user_model().objects.filter(
                email__iexact=self.cleaned_data['email']).exclude(
                    email__iexact=self.user.email):
            raise forms.ValidationError(
                _('This email is already in use. '
                  'Please supply a different email.'))
        return self.cleaned_data['email']

    def save(self):
        return self.user.userena_signup.change_email(
            self.cleaned_data['email'])
