from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from spokehub.profile.models import UserenaSignup
from spokehub.profile.utils import get_user_profile

invalid_username_message = (
    'Username must contain only letters, numbers, dots and underscores.')
USERNAME_RE = r'^[\.\w]+$'
attrs_dict = {'class': 'required'}

USERENA_ACTIVATION_REQUIRED = getattr(settings,
                                      'USERENA_ACTIVATION_REQUIRED',
                                      True)
USERENA_ACTIVATED = getattr(settings,
                            'USERENA_ACTIVATED',
                            'ALREADY_ACTIVATED')
USERENA_FORBIDDEN_USERNAMES = getattr(settings,
                                      'USERENA_FORBIDDEN_USERNAMES',
                                      ('signup', 'signout', 'signin',
                                       'activate', 'me', 'password'))


class SignupForm(forms.Form):
    username = forms.RegexField(
        regex=USERNAME_RE,
        max_length=30,
        widget=forms.TextInput(attrs=attrs_dict),
        label=_("Username"),
        error_messages={'invalid': _('Username must contain only letters'
                                     ', numbers, dots and underscores.')})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_("Email"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict,
                                                           render_value=False),
                                label=_("Create password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict,
                                                           render_value=False),
                                label=_("Repeat password"))

    def clean_username(self):
        try:
            get_user_model().objects.get(
                username__iexact=self.cleaned_data['username'])
        except get_user_model().DoesNotExist:
            pass
        else:
            if USERENA_ACTIVATION_REQUIRED and UserenaSignup.objects.filter(
                    user__username__iexact=self.cleaned_data['username']
            ).exclude(activation_key=USERENA_ACTIVATED):
                raise forms.ValidationError(
                    _('This username is already taken but not '
                      'confirmed. Please check your email for '
                      'verification steps.'))
            raise forms.ValidationError(_('This username is already taken.'))
        if self.cleaned_data['username'].lower() in \
           USERENA_FORBIDDEN_USERNAMES:
            raise forms.ValidationError(_('This username is not allowed.'))
        return self.cleaned_data['username']

    def clean_email(self):
        """ Validate that the e-mail address is unique. """
        if get_user_model().objects.filter(
                email__iexact=self.cleaned_data['email']):
            if (USERENA_ACTIVATION_REQUIRED and
                    UserenaSignup.objects.filter(
                        user__email__iexact=self.cleaned_data['email']
                    ).exclude(activation_key=USERENA_ACTIVATED)):
                raise forms.ValidationError(
                    _('This email is already in use but not confirmed. '
                      'Please check your email for verification steps.'))
            raise forms.ValidationError(
                _('This email is already in use. '
                  'Please supply a different email.'))
        return self.cleaned_data['email']

    def clean(self):
        if ('password1' in self.cleaned_data and 'password2'
                in self.cleaned_data):
            if self.cleaned_data['password1'] != \
                   self.cleaned_data['password2']:
                raise forms.ValidationError(
                    _('The two password fields didn\'t match.'))
        return self.cleaned_data

    def save(self):
        username, email, password = (self.cleaned_data['username'],
                                     self.cleaned_data['email'],
                                     self.cleaned_data['password1'])

        new_user = UserenaSignup.objects.create_user(
            username,
            email,
            password,
            not USERENA_ACTIVATION_REQUIRED,
            USERENA_ACTIVATION_REQUIRED)
        return new_user


class FullSignupForm(SignupForm):
    username = forms.RegexField(
        regex=USERNAME_RE,
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Username',
                                      'class': 'required'}),
        label="Username",
        error_messages={'invalid': invalid_username_message})
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password', 'class': 'required'},
            render_value=False),
        label="Create password")
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Repeat Password', 'class': 'required'},
            render_value=False),
        label="Repeat password")
    firstname = forms.CharField(
        label='First name', max_length=30, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                      'class': 'required'}),
        )
    lastname = forms.CharField(
        label='Last name', max_length=30, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                      'class': 'required'}))
    location = forms.CharField(
        label='City & Country', required=True,
        widget=forms.TextInput(attrs={'placeholder': 'City & country',
                                      'class': 'required'}))
    profession = forms.CharField(
        label='Profession', required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Profession',
                                      'class': 'required'}))
    website_url = forms.CharField(
        label='Website', required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Website',
                                      'class': 'required'}))
    website_name = forms.CharField(
        label='Website Name', required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Website Name',
                                      'class': 'required'}))
    email = forms.EmailField()

    profileimage = forms.FileField(
        widget=forms.FileInput(attrs={
            'id': "profile-image-upload",
            'accept': "image/*",
            'capture': "camera",
            'class': "inputfile-6",
            "data-multiple-caption": "{count} files selected",
            "multiple": "multiple"})
    )
    coverimage = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'id': "cover-image-upload",
            'accept': "image/*",
            'capture': "camera",
            'class': "inputfile-6",
            "data-multiple-caption": "{count} files selected",
            "multiple": "multiple"})
    )

    def save(self):
        new_user = super(FullSignupForm, self).save()

        new_user.first_name = self.cleaned_data['firstname']
        new_user.last_name = self.cleaned_data['lastname']
        new_user.save()

        user_profile = get_user_profile(new_user)
        user_profile.location = self.cleaned_data['location']
        user_profile.profession = self.cleaned_data['profession']
        user_profile.website_url = self.cleaned_data['website_url']
        user_profile.website_name = self.cleaned_data['website_name']
        user_profile.privacy = 'open'
        user_profile.save()
        return new_user

    def clean_website_url(self):
        if self.cleaned_data['website_url'].startswith('https://'):
            return self.cleaned_data['website_url']
        elif self.cleaned_data['website_url'].startswith('http://'):
            return self.cleaned_data['website_url']
        else:
            return 'http://' + self.cleaned_data['website_url']
