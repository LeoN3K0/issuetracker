from django.db import models
from member.models import CustomUser


class Project(models.Model):
    name = models.CharField('Project Name', max_length=120)
    project_id = models.CharField('Project ID', max_length=2)
    start_date = models.DateField('Start Date')
    end_date = models.DateField('Projected End Date')
    project_lead = models.ManyToManyField(CustomUser, limit_choices_to={'groups__name__in': ['Project Leaders', 'Admin']}, related_name='project_lead',)
    assigned_users = models.ManyToManyField(CustomUser, related_name='assigned_users')
    description = models.TextField('Description', blank=True)

    def __str__(self):
        return self.name

class Issue(models.Model):
    short_description = models.CharField('Issue Name', max_length=200)
    issue_date = models.DateTimeField('Issue Date')
    issue_date_complete = models.DateTimeField('Fixed Date', blank=True)
    description = models.TextField('Description')
    related_project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    issue_id = models.CharField('Issue ID', max_length=999)
    fixed_issue = models.BooleanField('Fixed Issue', blank=True)

    def __str__(self):
        return self.short_description