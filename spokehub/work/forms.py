from django.forms import ModelForm, TextInput

from .models import Project


widgets_map = {
    'slug': TextInput(),
    'title': TextInput(),
    'subhead': TextInput(),
    'date': TextInput(),
}


class EditProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'subhead', 'date', 'description']
        widgets = widgets_map


class CreateProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['slug', 'title', 'subhead', 'date', 'description']
        widgets = widgets_map
