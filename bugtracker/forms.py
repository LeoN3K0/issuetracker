from django import forms
from django.forms import ModelForm
from django.db.models import Q
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django_select2.forms import Select2MultipleWidget, Select2Widget
from django_select2 import forms as s2forms
from .models import Project, Issue, CustomUser


class SearchUserWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "full_name__icontains",
        "email__icontains",
    ]


#Project Forms
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'start_date', 'end_date', 'project_lead', 'assigned_users', 'description', 'creation_date')
        labels = {
            'name': '',
            'description': '',
            'start_date': '',
            'end_date': '',
            'project_lead': '',
            'assigned_users': ''
        }
        help_texts = {
            'project_lead': 'Search and Assign Multiple Leaders.',
            'assigned_users': 'Search and Assign Multiple Users.',
        }
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control-sm", 'placeholder': 'Name'}),
            'description': forms.Textarea(attrs={"class": "form-control-md", 'placeholder': 'Description'}),
            'start_date': DatePickerInput(attrs={"class": "form-control-sm", 'placeholder': 'Start Date'}),
            'end_date': DatePickerInput(attrs={"class": "form-control-sm", 'placeholder': 'Projected End Date'}),
            'project_lead': SearchUserWidget(attrs={'data-placeholder': 'Assign Project Leaders', 'data-width': 'resolve'}),
            'assigned_users': SearchUserWidget(attrs={'data-placeholder': 'Assign Users', 'data-width': 'resolve'}),
            'creation_date': forms.HiddenInput(),

        }


#Issues Forms
class TicketForm(ModelForm):
    class Meta:
        model = Issue
        fields = ('issue_date', 'related_project', 'description', 'submitter', 'priority')
        exclude = ('fixed_by',)
        labels = {
            'issue_date': '',
            'related_project': '',
            'description': '',
            'priority': '',
        }
        widgets = {
            'description': forms.Textarea(attrs={"class": "form-control-md", 'placeholder': 'Describe the issue in detail'}),
            'issue_date': forms.HiddenInput(),
            'related_project': Select2Widget(attrs={"class": "form-control-sm", 'data-placeholder': 'Project with Issue'}),
            'submitter': forms.HiddenInput(),
            'priority': Select2Widget(attrs={"class": "form-control-md"}),

        }


class TicketAssignForm(ModelForm):
    class Meta:
        model = Issue
        fields = ('assigned_users',)
        labels = {
            'assigned_users': '',
        }
        widgets = {
            'assigned_users': Select2MultipleWidget(attrs={'data-placeholder': 'Assign Users', 'data-width': '90%'}),

        }


class TicketEditForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fixed_comment'].required = True

    class Meta:
        model = Issue
        fields = ('fixed_comment', 'issue_fixed', 'priority', 'fixed_by', 'issue_date_complete', 'closed_by', 'closed_date',)
        labels = {
            'fixed_comment': '',
            'issue_fixed': 'Progress',
            'priority': 'Priority',
        }
        help_texts = {'fixed_comment': 'Comment on change of progress if, closing for what reason'}
        widgets = {
            'fixed_comment': forms.Textarea(attrs={"class": "form-control-md", 'placeholder': 'Ticket Comments'}),
            'issue_fixed': Select2Widget(attrs={"class": "form-control-md"}),
            'priority': Select2Widget(attrs={"class": "form-control-md"}),
            'fixed_by': forms.HiddenInput(),
            'issue_date_complete': forms.HiddenInput(),
            'closed_by': forms.HiddenInput(),
            'closed_date': forms.HiddenInput(),

        }


class SpcTicketForm(ModelForm):
    class Meta:
        model = Issue
        fields = ('fixed_comment',)
        labels = {
            'fixed_comment': '',
        }
        widgets = {
            'fixed_comment': forms.Textarea(attrs={"class": "form-control-plaintext", 'readonly': 'readonly',
                                                   'style': 'resize:none', 'rows': 4, })
        }



