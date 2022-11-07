import django_tables2 as tables
from .models import Project, Issue
from django.urls import reverse
from django.utils.html import format_html
from member.models import CustomUser


# Project Tables
class ProjectTable(tables.Table):
    class Meta:
        orderable = True
        model = Project
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ("name", "project_lead", "start_date", "end_date", "description")
        exclude = ("project_id", "assigned_users",)
        attrs = {'class': 'table table-hover', 'thead': {'class': 'thead-light'}}

    def render_name(self, record):
        return format_html('<a href="{}">{}</a>',
                           reverse('project_page',
                                   kwargs={'name': record.name}), record.name)


class ProjectsList(tables.Table):
    class Meta:
        orderable = True
        model = Project
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ("name", "start_date", "end_date")
        exclude = ("project_id", "assigned_users",)
        attrs = {'class': 'table table-hover table-borderless'}


    def render_name(self, record):
        return format_html('<a href="{}">{}</a>',
                           reverse('project_page',
                                   kwargs={'name': record.name}), record.name)


class ProjectTableCard(tables.Table):
    class Meta:
        orderable = True
        model = Project
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "start_date", "end_date", "description")
        exclude = ("project_id", "assigned_users", "project_lead",)


class LeaderCard(tables.Table):
    class Meta:

        model = CustomUser
        template_name = "django_tables2/bootstrap-responsive-custom.html"
        fields = ("full_name",)
        attrs = {'class': 'table table-borderless'}


class AssignedCard(tables.Table):
    class Meta:
        model = CustomUser
        template_name = "django_tables2/bootstrap-responsive-custom.html"
        fields = ("full_name",)
        attrs = {'class': 'table table-borderless'}


#Issue Tables
class IssueTable(tables.Table):
    class Meta:
        orderable = True
        model = Issue
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ('ticket_id', 'issue_date', 'related_project', 'description', 'issue_date_complete', 'issue_fixed')
        exclude = ('issue_id',)

    def render_ticket_id(self, record):
        return format_html('<a href="{}">{}</a>',
                           reverse('ticket_page',
                                   kwargs={'ticket_id': record.ticket_id}), record.ticket_id)


class TicketsByProjects(tables.Table):
    class Meta:
        orderable = True
        model = Issue
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ('ticket_id', 'related_project', 'issue_fixed', 'priority')
        exclude = ('issue_id',)
        attrs = {'class': 'table table-borderless'}
        row_attrs = {
            "style": lambda
                record: "background-color: rgb(255, 36, 0, 0.2);" if record.priority == "High" and record.issue_fixed != "Closed" and record.issue_fixed != "Fixed" else "background-color: rgb(125, 249, 255, 0.5);"
            if record.priority == "Low" and record.issue_fixed != "Closed" and record.issue_fixed != "Fixed" else "background-color: rgb(253, 218, 13, 0.5);" if record.priority == "Medium" and record.issue_fixed != "Closed" and record.issue_fixed != "Fixed"
            else "background-color: rgb(11, 218, 81, 0.2);" if record.issue_fixed == "Closed" or record.issue_fixed == "Fixed" else ""
        }

    def render_ticket_id(self, record):
        return format_html('<a href="{}">{}</a>',
                           reverse('ticket_page',
                                   kwargs={'ticket_id': record.ticket_id}), record.ticket_id)


class AssignedTickets(tables.Table):
    class Meta:
        orderable = True
        model = Issue
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ('ticket_id', 'issue_fixed', 'priority')
        exclude = ('issue_id',)
        attrs = {'class': 'table table-borderless'}
        row_attrs = {
            "style": lambda
                record: "background-color: rgb(255, 36, 0, 0.2);" if record.priority == "High" and record.issue_fixed != "Closed" and record.issue_fixed != "Fixed" else "background-color: rgb(125, 249, 255, 0.5);"
            if record.priority == "Low" and record.issue_fixed != "Closed" and record.issue_fixed != "Fixed" else "background-color: rgb(253, 218, 13, 0.5);" if record.priority == "Medium" and record.issue_fixed != "Closed" and record.issue_fixed != "Fixed"
            else "background-color: rgb(11, 218, 81, 0.2);" if record.issue_fixed == "Closed" or record.issue_fixed == "Fixed" else ""
        }

    def render_ticket_id(self, record):
        return format_html('<a href="{}">{}</a>',
                           reverse('ticket_page',
                                   kwargs={'ticket_id': record.ticket_id}), record.ticket_id)


class SubmittedTickets(tables.Table):
    class Meta:
        orderable = True
        model = Issue
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ('ticket_id', 'issue_date', 'issue_date_complete', 'issue_fixed', 'priority')
        exclude = ('issue_id',)
        attrs = {'class': 'table table-borderless'}
        row_attrs = {
            "style": lambda
                record: "background-color: rgb(255, 36, 0, 0.2);" if record.priority == "High" and record.issue_fixed != "Closed" and record.issue_fixed != "Fixed" else "background-color: rgb(125, 249, 255, 0.5);"
            if record.priority == "Low" and record.issue_fixed != "Closed" and record.issue_fixed != "Fixed" else "background-color: rgb(253, 218, 13, 0.5);" if record.priority == "Medium" and record.issue_fixed != "Closed" and record.issue_fixed != "Fixed"
            else "background-color: rgb(11, 218, 81, 0.2);" if record.issue_fixed == "Closed" or record.issue_fixed == "Fixed" else ""
        }

    def render_ticket_id(self, record):
        return format_html('<a href="{}">{}</a>',
                           reverse('ticket_page',
                                   kwargs={'ticket_id': record.ticket_id}), record.ticket_id)

