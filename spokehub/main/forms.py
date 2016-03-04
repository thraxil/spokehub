from django import forms
from .models import Reply


class ReplyUpdateForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['body', 'image', 'url', 'youtube_id', 'vimeo_id']
