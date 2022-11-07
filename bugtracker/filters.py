import django_filters as filter1
from .models import Project


class ProjectFilter(filter1.FilterSet):
    class Meta:
        model = Project
        fields = ['name', 'start_date']