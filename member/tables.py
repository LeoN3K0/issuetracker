import django_tables2 as tables
from .models import AccessRequest


# Project Tables
class RequestTable(tables.Table):
    accept = tables.TemplateColumn(template_name='extra/accept.html')
    deny = tables.TemplateColumn(template_name='extra/deny.html')
    class Meta:
        orderable = True
        model = AccessRequest
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ("first_name", "last_name", "request_date", "reason", "accept", "deny")
        attrs = {'class': 'table table-hover', 'thead': {'class': 'thead-light'}}

