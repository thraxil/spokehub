from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from spokehub.work.models import Project
from spokehub.work.forms import EditProjectForm, CreateProjectForm


class IndexView(TemplateView):
    template_name = "edit/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        return context


class AddProjectView(SuccessMessageMixin, CreateView):
    template_name = "edit/add_project.html"
    model = Project
    form_class = CreateProjectForm
    success_url = reverse_lazy('edit-index')
    success_message = "%(title)s was created successfully"

    def form_valid(self, form):
        if 'thumbnail' in self.request.FILES:
            image = self.request.FILES['thumbnail']
            form.instance.save_thumbnail(image)
        return super(AddProjectView, self).form_valid(form)


class ProjectUpdate(SuccessMessageMixin, UpdateView):
    model = Project
    form_class = EditProjectForm
    success_url = reverse_lazy('edit-index')
    success_message = "%(title)s updated"

    def form_valid(self, form):
        if 'thumbnail' in self.request.FILES:
            image = self.request.FILES['thumbnail']
            form.instance.save_thumbnail(image)
        return super(ProjectUpdate, self).form_valid(form)


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('edit-index')
    success_message = "Project Deleted"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ProjectDelete, self).delete(request, *args, **kwargs)
