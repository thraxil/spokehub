from django.forms import CharField
from userena.forms import EditProfileForm


class ExtendedEditProfileForm(EditProfileForm):
    first_name = CharField(label='First name', max_length=30, required=True)
    last_name = CharField(label='Last name', max_length=30, required=True)
