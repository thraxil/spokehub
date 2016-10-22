from django.forms import ModelForm, TextInput

from .models import Project


class EditProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'subhead', 'date', 'description']

        widgets = {
            'title': TextInput(),
            'subhead': TextInput(),
            'date': TextInput(),
        }
