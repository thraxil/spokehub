from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from spokehub.work.models import Project
from spokehub.work.forms import EditProjectForm, CreateProjectForm


class IndexView(TemplateView):
    template_name = "edit/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        return context


class AddProjectView(CreateView):
    template_name = "edit/add_project.html"
    model = Project
    form_class = CreateProjectForm
    success_url = reverse_lazy('edit-index')


class ProjectUpdate(UpdateView):
    model = Project
    form_class = EditProjectForm
    success_url = reverse_lazy('edit-index')
