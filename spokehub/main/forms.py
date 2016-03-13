from django import forms
from userena.forms import AuthenticationForm
from .models import Reply, Conversation


class ReplyUpdateForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['image', 'url', 'body']
        widgets = {
            'url': forms.TextInput(attrs=dict(maxlength=140)),
            'body': forms.Textarea(attrs=dict(maxlength=140)),
        }


class ConversationUpdateForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs=dict(maxlength=140)),
        }


class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        widget=forms.HiddenInput(),
        required=False,
        initial=True,
        label="",
        )

    def __init__(self, *args, **kwargs):
        """ AuthenticationForm.__init__() sets the label on remember_me
        so we need to override it to keep it empty for the hidden field """
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        return None
