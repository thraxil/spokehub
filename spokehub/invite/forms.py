from django import forms
from userena.forms import SignupForm, USERNAME_RE
from userena.utils import get_user_profile

invalid_username_message = (
    'Username must contain only letters, numbers, dots and underscores.')


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
