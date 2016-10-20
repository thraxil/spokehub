from django.contrib import admin
from .models import Project, ProjectContributor, ProjectMedia

admin.site.register(Project)
admin.site.register(ProjectContributor)
admin.site.register(ProjectMedia)
