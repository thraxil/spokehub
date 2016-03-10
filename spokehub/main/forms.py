from django import forms
from .models import Reply


class ReplyUpdateForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['image', 'url', 'body']
        widgets = {
            'url': forms.TextInput(attrs=dict(maxlength=140)),
        }
