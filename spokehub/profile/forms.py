from django.forms import CharField
from userena.forms import EditProfileForm


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
