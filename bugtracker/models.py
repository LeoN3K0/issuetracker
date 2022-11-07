import random
import string
from django.db import models
from member.models import CustomUser
from django.core.validators import MinLengthValidator


def random_id_string():
    return random.choice(string.ascii_letters) + str(random.randint(1, 9)) + random.choice(string.ascii_letters)


class Project(models.Model):
    name = models.CharField('Project Name', max_length=120)
    project_id = models.CharField('Project ID', max_length=3,  unique=True, blank=True, default=random_id_string,)
    start_date = models.DateField('Start Date')
    end_date = models.DateField('Projected End Date')
    project_lead = models.ManyToManyField(CustomUser, limit_choices_to={'groups__name__in': ['Project Leaders', 'Admin']}, related_name='project_lead')
    assigned_users = models.ManyToManyField(CustomUser, related_name='assigned_users', blank=True)
    description = models.TextField('Description', blank=True)
    creation_date = models.DateTimeField('Date Created', blank=True, null=True,)

    def __str__(self):
        return self.name


def random_string():
    return str(random.randint(1000, 99999))


class Issue(models.Model):
    priority_choices = [('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')]
    progress_choices = [
        ('Open', 'Open'), ('In Progress', 'In Progress'), ('Closed', 'Closed'),
        ('Fixed', 'Fixed'), ('On Hold', 'On Hold'), ('Duplicate', 'Duplicate')
    ]

    issue_date = models.DateTimeField('Issue Date', blank=True)
    issue_date_complete = models.DateField('Fixed Date', blank=True, null=True)
    description = models.TextField('Description')
    related_project = models.ForeignKey(Project, default=None, on_delete=models.CASCADE)
    issue_id = models.CharField(default=random_string, max_length=999999)
    ticket_id = models.CharField('Ticket ID', max_length=9999999, blank=True, unique=True)
    issue_fixed = models.CharField('Ticket Progress', max_length=100, choices=progress_choices, default='Open')
    fixed_comment = models.TextField('Comment', blank=True)
    submitter = models.ForeignKey(CustomUser, default=None, blank=True, on_delete=models.CASCADE)
    assigned_users = models.ManyToManyField(CustomUser, related_name='working_users', blank=True,)
    fixed_by = models.ForeignKey(CustomUser, default=None, blank=True, null=True, on_delete=models.CASCADE, related_name='fixed_by',)
    priority = models.CharField(max_length=60, choices=priority_choices, default='Medium')
    closed_by = models.ForeignKey(CustomUser, default=None, blank=True, null=True, on_delete=models.CASCADE, related_name='closed_by',)
    closed_date = models.DateField('Closed Date', blank=True, null=True)

    def __str__(self):
        return self.ticket_id

    def save(self, *args, **kwargs):
        self.ticket_id = self.related_project.project_id + self.issue_id
        super().save(*args, **kwargs)


