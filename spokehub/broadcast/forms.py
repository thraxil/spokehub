from django import forms


class BroadcastForm(forms.Form):
    subject = forms.CharField(label='Subject', required=True)
    body = forms.CharField(
        label='message body',
        required=True,
        widget=forms.Textarea(attrs={'style': 'width: 100%'}),
    )
