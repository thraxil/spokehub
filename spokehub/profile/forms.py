from django import forms
from userena.forms import EditProfileForm


class ExtendedEditProfileForm(EditProfileForm):
    first_name = forms.CharField(label='First name',
                                 max_length=30,
                                 required=True)
    last_name = forms.CharField(label='Last name',
                                max_length=30,
                                required=True)
