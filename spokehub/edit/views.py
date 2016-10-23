from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from spokehub.work.models import Project, ProjectContributor, ProjectMedia
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

    def get_context_data(self, **kwargs):
        context = super(ProjectUpdate, self).get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context

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


class ProjectAddContributor(View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        user = request.POST.get('user')
        fullname = request.POST.get('fullname')
        project.projectcontributor_set.create(
            user_id=user,
            fullname=fullname,
        )
        messages.success(self.request, "contributor added")
        return HttpResponseRedirect(reverse('edit-project', args=[pk, ]))


class ProjectAddMedia(View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if 'image' in request.FILES:
            image = request.FILES['image']
            project.add_image(image)
            messages.success(request, "image added")
        youtube_url = request.POST.get('youtube_url', "")
        if youtube_url != "":
            project.add_youtube(youtube_url)
            messages.success(self.request, "youtube video added")
        vimeo_url = request.POST.get('vimeo_url', "")
        if vimeo_url != "":
            project.add_vimeo(vimeo_url)
            messages.success(self.request, "vimeo video added")
        return HttpResponseRedirect(reverse('edit-project', args=[pk, ]))


class ProjectPublish(View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.publish()
        messages.success(self.request, "project published")
        return HttpResponseRedirect(reverse('edit-project', args=[pk, ]))


class ProjectDraft(View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.draft()
        messages.success(self.request, "project reverted to draft")
        return HttpResponseRedirect(reverse('edit-project', args=[pk, ]))


class ProjectContributorDelete(DeleteView):
    model = ProjectContributor
    success_message = "Contributor Removed"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ProjectContributorDelete, self).delete(
            request, *args, **kwargs)

    def get_success_url(self):
        return reverse('edit-project', args=[self.object.project.pk])


class ProjectMediaDelete(DeleteView):
    model = ProjectMedia
    success_message = "Media Removed"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ProjectMediaDelete, self).delete(
            request, *args, **kwargs)

    def get_success_url(self):
        return reverse('edit-project', args=[self.object.project.pk])


class ReorderProjectMedia(View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        keys = [int(k[len('media_'):]) for k in request.POST.keys()]
        keys.sort()
        sis = [int(request.POST["media_%d" % k]) for k in keys]
        project.set_projectmedia_order(sis)
        return HttpResponse(status=200)
