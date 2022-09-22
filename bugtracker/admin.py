from django.contrib import admin
from .models import Project, Issue
from member.models import CustomUser

admin.site.register(Project)
admin.site.register(Issue)
