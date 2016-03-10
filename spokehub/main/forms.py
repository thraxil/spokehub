from django import forms
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
