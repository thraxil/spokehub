from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from spokehub.work.models import Project


class AddProjectView(View):
    template_name = "edit/add_project.html"

    def get(self, request):
        return render(request, self.template_name, dict())

    def post(self, request):
        slug = request.POST.get('slug')
        title = request.POST.get('title')
        subhead = request.POST.get('subhead')
        date = request.POST.get('date')
        description = request.POST.get('description')
        Project.objects.create(
            slug=slug, title=title, subhead=subhead,
            date=date, description=description)
        return HttpResponseRedirect(reverse('edit-index', args=[]))
