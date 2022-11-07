import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django_tables2 import RequestConfig
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Project, Issue, CustomUser
from .tables import ProjectTable, IssueTable, LeaderCard, AssignedCard, TicketsByProjects, AssignedTickets, SubmittedTickets
from .forms import ProjectForm, TicketForm, TicketAssignForm, TicketEditForm, SpcTicketForm
from datetime import date, datetime

@login_required(login_url='login_register')
def search_site(request):
    if request.method == "POST":
        searched = request.POST['searched']
        if not request.user.groups.filter(name='Admin'):
            try:
                searched_date = datetime.strptime(searched, '%m/%d/%Y')
                project = Project.objects.filter(Q(creation_date__date=searched_date) &
                                                         Q(Q(assigned_users=request.user) | Q(
                                                             project_lead=request.user))).distinct().values_list('name', flat=True)
                tickets = Issue.objects.filter(Q(issue_date__date=searched_date) &
                                                       Q(Q(related_project__assigned_users=request.user) | Q(
                                                           related_project__project_lead=request.user))).distinct().values_list('ticket_id',
                                                                                                      flat=True)
            except:
                try:
                    searched_month = datetime.strptime(searched, '%b')
                    project = Project.objects.filter(Q(creation_date__month=searched_month.month) &
                                                         Q(Q(assigned_users=request.user) | Q(
                                                             project_lead=request.user))).distinct().values_list('name', flat=True)
                    tickets = Issue.objects.filter(Q(issue_date__month=searched_month.month) &
                                                       Q(Q(related_project__assigned_users=request.user) | Q(
                                                           related_project__project_lead=request.user))).distinct().values_list('ticket_id',
                                                                                                        flat=True)
                except:
                    try:
                        search_month = datetime.strptime(searched, '%B')
                        project = Project.objects.filter(Q(creation_date__month=search_month.month) &
                                                         Q(Q(assigned_users=request.user) | Q(
                                                             project_lead=request.user))).distinct().values_list(
                            'name', flat=True)
                        tickets = Issue.objects.filter(Q(issue_date__month=search_month.month)&
                                                       Q(Q(related_project__assigned_users=request.user) | Q(
                                                           related_project__project_lead=request.user))).distinct().values_list('ticket_id',
                                                                                                     flat=True)
                    except:
                        project = Project.objects.filter(Q(name__icontains=searched) &
                                                         Q(Q(assigned_users=request.user) | Q(
                                                             project_lead=request.user))).distinct().values_list('name',
                                                                                                                 flat=True)
                        tickets = Issue.objects.filter(Q(ticket_id__icontains=searched) &
                                                       Q(Q(related_project__assigned_users=request.user) | Q(
                                                           related_project__project_lead=request.user))).distinct().values_list(
                            'ticket_id', flat=True)
        else:
            try:
                searched_date = datetime.strptime(searched, '%m/%d/%Y')
                project = Project.objects.filter(Q(creation_date__date=searched_date)).values_list('name', flat=True)
                tickets = Issue.objects.filter(Q(issue_date__date=searched_date)).values_list('ticket_id',
                                                                                                      flat=True)
            except:
                try:
                    searched_month = datetime.strptime(searched, '%b')
                    project = Project.objects.filter(Q(creation_date__month=searched_month.month)).values_list('name', flat=True)
                    tickets = Issue.objects.filter(Q(issue_date__month=searched_month.month)).values_list('ticket_id',
                                                                                                        flat=True)
                except:
                    try:
                        search_month = datetime.strptime(searched, '%B')
                        project = Project.objects.filter(Q(creation_date__month=search_month.month)).values_list(
                            'name', flat=True)
                        tickets = Issue.objects.filter(Q(issue_date__month=search_month.month)).values_list('ticket_id',
                                                                                                     flat=True)
                    except:
                        project = Project.objects.filter(Q(name__icontains=searched)).values_list('name', flat=True)
                        tickets = Issue.objects.filter(Q(ticket_id__icontains=searched)).values_list('ticket_id',
                                                                                                     flat=True)
        project_list = [pl for pl in project]
        ticket_list = [it for it in tickets]
        search_list = project_list + ticket_list
        search_list_num = len(search_list)
        context = {
            'searched': searched,
            'search_list_num': search_list_num,
            'search_list': search_list,
            'project_list': project_list,
            'ticket_list': ticket_list,
        }
        return render(request, 'bugs/search_site.html', context)
    else:
        return render(request, 'bugs/search_site.html')



#Index view
class ChartData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        admin = request.user.groups.filter(name__exact='Admin')
        projects = Project.objects.filter(project_lead=request.user)
        projectsLead = Project.objects.filter(project_lead=request.user).order_by(
            '-creation_date').values_list('name', flat=True).distinct()[:2]
        leadData = Project.objects.filter(project_lead=request.user).order_by(
            '-creation_date').annotate(issue_count=Count('issue'))[:2]
        leadData1 = Project.objects.filter(project_lead=request.user).order_by(
            '-creation_date').annotate(issue_count=Count('issue', filter=Q(issue__issue_fixed='Fixed')))[:2]
        leadData2 = Project.objects.filter(project_lead=request.user).order_by(
            '-creation_date').annotate(issue_count=Count('issue', filter=Q(issue__issue_fixed='Closed')))[:2]
        if projects:
            projectsAssigned = Project.objects.filter(assigned_users=request.user).order_by(
                '-creation_date').values_list('name', flat=True).distinct()[:2]
            assignedData =Project.objects.filter(assigned_users=request.user).order_by(
            '-creation_date').annotate(issue_count=Count('issue'))[:2]
            assignedData1 = Project.objects.filter(assigned_users=request.user).order_by(
                '-creation_date').annotate(issue_count=Count('issue', filter=Q(issue__issue_fixed='Fixed')))[:2]
            assignedData2 = Project.objects.filter(assigned_users=request.user).order_by(
                '-creation_date').annotate(issue_count=Count('issue', filter=Q(issue__issue_fixed='Closed')))[:2]

        elif admin:
            projectsAssigned = Project.objects.all().order_by(
                '-creation_date').values_list('name', flat=True)[:4]
            assignedData = Project.objects.all().order_by(
                '-creation_date').annotate(issue_count=Count('issue'))[:4]
            assignedData1 = Project.objects.all().order_by(
                '-creation_date').annotate(issue_count=Count('issue', filter=Q(issue__issue_fixed='Fixed')))[:4]
            assignedData2 = Project.objects.all().order_by(
                '-creation_date').annotate(issue_count=Count('issue', filter=Q(issue__issue_fixed='Closed')))[:4]
        else:
            projectsAssigned = Project.objects.filter(assigned_users=request.user).order_by(
                '-creation_date').values_list('name', flat=True)[:4]
            assignedData = Project.objects.filter(assigned_users=request.user).order_by(
                '-creation_date').annotate(issue_count=Count('issue'))[:4]
            assignedData1 = Project.objects.filter(assigned_users=request.user).order_by(
                '-creation_date').annotate(issue_count=Count('issue', filter=Q(issue__issue_fixed='Fixed')))[:4]
            assignedData2 = Project.objects.filter(assigned_users=request.user).order_by(
                '-creation_date').annotate(issue_count=Count('issue', filter=Q(issue__issue_fixed='Closed')))[:4]

        cht1labels = ["High", "Medium", "Low"]
        cht1data = [self.getPriority(request, priority=cht1labels[0]), self.getPriority(request, priority=cht1labels[1]),
                    self.getPriority(request, priority=cht1labels[2])]
        cht2labels = ['Open', 'In Progress', 'On Hold', 'Duplicate', 'Fixed', 'Closed']
        cht2data = [self.getStatus(request, status=cht2labels[0]), self.getStatus(request, status=cht2labels[1]), self.getStatus(request, status=cht2labels[2]),
                    self.getStatus(request, status=cht2labels[3]), self.getStatus(request, status=cht2labels[4]), self.getStatus(request, status=cht2labels[5])]
        leadlabels = [pl for pl in projectsLead]
        assignedLabels = [pa for pa in projectsAssigned]
        cleadData = [ld.issue_count for ld in leadData]
        cleadData1 = [ld.issue_count for ld in leadData1]
        cleadData2 = [ld.issue_count for ld in leadData2]
        cassignedData = [ad.issue_count for ad in assignedData]
        cassignedData1 = [ad.issue_count for ad in assignedData1]
        cassignedData2 = [ad.issue_count for ad in assignedData2]


        cht4labels = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        cht4data = [self.getMonth(request, 1), self.getMonth(request, 2), self.getMonth(request, 3),
                    self.getMonth(request, 4), self.getMonth(request, 5), self.getMonth(request, 6),
                    self.getMonth(request, 7), self.getMonth(request, 8), self.getMonth(request, 9),
                    self.getMonth(request, 10), self.getMonth(request, 11), self.getMonth(request, 12)]
        if projects:
            cht3labels = list(dict.fromkeys(leadlabels + assignedLabels))
            cht3data = cleadData + cassignedData
            cht3data1 = cleadData1 + cassignedData1
            cht3data2 = cleadData2 + cassignedData2
        else:
            cht3labels = assignedLabels
            cht3data = cassignedData
            cht3data1 = cassignedData1
            cht3data2 = cassignedData2
        data = {
            'cht1labels': cht1labels,
            'cht1data': cht1data,
            'cht2labels': cht2labels,
            'cht2data': cht2data,
            'cht3labels': cht3labels,
            'cht3data': cht3data,
            'cht3data1': cht3data1,
            'cht3data2': cht3data2,
            'cht4labels': cht4labels,
            'cht4data': cht4data
        }
        return Response(data)

    def getPriority(self, request, priority):
        if request.user.groups.filter(name__exact='Admin'):
            querryset = Issue.objects.filter(Q(priority=priority)).count()
        else:
            querryset = Issue.objects.filter(Q(priority=priority) & Q(assigned_users=request.user)).distinct().count()
        return querryset
    def getStatus(self, request, status):
        if status == 'Open':
            querryset = Issue.objects.filter(Q(issue_fixed=status) & Q(Q(related_project__assigned_users=request.user) |
                                                                       Q(related_project__project_lead=request.user))).distinct().count()
        elif request.user.groups.filter(name__exact='Admin'):
            querryset = Issue.objects.filter(Q(issue_fixed=status)).count()
        else:
            querryset = Issue.objects.filter(Q(issue_fixed=status) & Q(assigned_users=request.user)).distinct().count()

        return querryset

    def getMonth(self, request, month):
        today = date.today()
        year = today.year

        if request.user.groups.filter(name__exact='Admin'):
            querryset = Issue.objects.filter(issue_date__year=year, issue_date__month=month).count()
        else:
            querryset = Issue.objects.filter(Q(issue_date__year=year, issue_date__month=month) &
                                             Q(Q(related_project__project_lead=request.user) | Q(
                                                 related_project__assigned_users=request.user))).count()
        return querryset

@login_required(login_url='login_register')
def bugtracker(request):
    admin = request.user.groups.filter(name__exact='Admin')
    context = {
        'admin': admin
    }
    return render(request, 'bugs/main_index.html', context)

#Project Related Views
@login_required(login_url='login_register')
def projects_table_page(request):
    project_card1 = Project.objects.none()
    related_user = Project.assigned_users
    related_leader = Project.project_lead
    user_group = request.user.groups
    table = ProjectTable(project_card1)
    user = request.user
    RequestConfig(request).configure(table)
    if user_group.filter(name__exact='General User'):
        if related_user == user:
            project_card = Project.objects.filter(assigned_users__email__exact=user.email)
            table = ProjectTable(project_card)
            RequestConfig(request).configure(table)
        else:
            project_card = Project.objects.filter(assigned_users__email__exact=user.email)
            table = ProjectTable(project_card)
            RequestConfig(request).configure(table)
    elif user_group.filter(name__exact='Project Leaders'):
        if related_leader == user:
            project_card = Project.objects.filter(project_lead__email__exact=user.email)
            table = ProjectTable(project_card)
            RequestConfig(request).configure(table)
        else:
            project_card = Project.objects.filter(Q(assigned_users__email__exact=user.email) | Q(project_lead__email__exact=user.email))
            table = ProjectTable(project_card)
            RequestConfig(request).configure(table)
    elif user_group.filter(name__exact='Admin'):
        project_card = Project.objects.all()
        table = ProjectTable(project_card)
        RequestConfig(request).configure(table)

    return render(request, 'bugs/projects.html', {'table': table})

@login_required(login_url='login_register')
def add_project_page(request):
    submitted = False
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            creation = form.save(commit=False)
            creation.creation_date = datetime.now()
            creation.save()
            form.save()
            messages.success(request, 'Project has been created succesfully')
            return HttpResponseRedirect('?submitted=True')

    else:
        form = ProjectForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'bugs/add_projects.html', {'form': form, 'submitted': submitted})


@login_required(login_url='login_register')
def project_page(request, name):
    user_groups = request.user.groups.filter(name__exact='General User')
    admin = request.user.groups.filter(name__exact='Admin')
    issueticket = Issue.objects.filter(related_project__name__exact=name)
    issuetable = IssueTable(issueticket)
    project = get_object_or_404(Project, name=name)
    leaders = project.project_lead.filter(full_name__exact=request.user.full_name)
    lead = project.project_lead.all()
    leader_table = LeaderCard(lead)
    assigned = project.assigned_users.all()
    assigned_table = AssignedCard(assigned)
    project_assign = project.assigned_users.filter(full_name__exact=request.user.full_name)
    project_assign1 = project.project_lead.filter(full_name__exact=request.user.full_name)
    form = TicketForm(request.POST or None, initial={'related_project': project})

    if 'submit_ticket' in request.POST:
        if form.is_valid():
            submitter = form.save(commit=False)
            submitter.submitter = request.user
            submitter.issue_date = datetime.now()
            submitter.save()
            messages.success(request, 'Ticket has been submitted')
            return redirect('project_page', project.name)

    context = {
        'name': name,
        'project': project,
        'issuetable': issuetable,
        'leaders': leaders,
        'admin': admin,
        'user_groups': user_groups,
        'leader_table': leader_table,
        'assigned_table': assigned_table,
        'form': form,
    }

    if project_assign or project_assign1:
        return render(request, 'bugs/main_projects.html', context)
    elif admin:
        return render(request, 'bugs/main_projects.html', context)
    else:
        return redirect('projects')




@login_required(login_url='login_register')
def delete_project(request, name):
    project = Project.objects.get(name=name)
    project.delete()

    return redirect('projects')


@login_required(login_url='login_register')
def update_project(request, name):
    project = Project.objects.get(name=name)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect('projects')

    return render(request, 'bugs/update_projects.html', {'project': project, 'form': form})


#Issue related Views
@login_required(login_url='login_register')
def issues_table_page(request):
    user = request.user
    user_group = request.user.groups
    submittedticket = Issue.objects.filter(submitter=user)
    assignedticket = Issue.objects.filter(assigned_users=user)
    assigned_table = AssignedTickets(assignedticket)
    RequestConfig(request).configure(assigned_table)
    submitted_table = SubmittedTickets(submittedticket)
    RequestConfig(request).configure(submitted_table)
    ticketbyproject = Issue.objects.filter(Q(related_project__assigned_users__email__exact=user.email) |
                                           Q(related_project__project_lead__email__exact=user.email)).distinct()

    ticket_table = TicketsByProjects(ticketbyproject)
    RequestConfig(request).configure(ticket_table)

    context = {
        'ticket_table': ticket_table,
        'submitted_table': submitted_table,
        'assigned_table': assigned_table,
    }

    return render(request, 'bugs/issues.html', context)

@login_required(login_url='login_register')
def submit_ticket_page(request):
    form = TicketForm(request.POST)
    form.fields['related_project'].queryset = Project.objects.filter(Q(assigned_users=request.user) |
                                                                     Q(project_lead=request.user)).distinct()
    submitted = False
    if request.method == "POST":
        if form.is_valid():
            submitter = form.save(commit=False)
            submitter.submitter = request.user
            submitter.issue_date = datetime.now()
            submitter.save()
            messages.success(request, 'Ticket has been submitted')
            return HttpResponseRedirect('?submitted=True')

    else:
        form = TicketForm()
        form.fields['related_project'].queryset = Project.objects.filter(Q(assigned_users=request.user) |
                                                                         Q(project_lead=request.user)).distinct()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'bugs/submit_ticket.html', {'form': form, 'submitted': submitted})


@login_required(login_url='login_register')
def ticket_page(request, ticket_id):
    user_groups = request.user.groups.filter(Q(name__exact='Admin') | Q(name__exact='Project Leaders'))
    admin = request.user.groups.filter(name__exact='Admin')
    issue = get_object_or_404(Issue, ticket_id=ticket_id)
    project = get_object_or_404(Project, name=issue.related_project.name)
    submitter = issue.submitter
    assigned = issue.assigned_users.all()
    assigned1 = issue.assigned_users.exists()
    assigned2 = issue.assigned_users.filter(full_name__exact=request.user.full_name)
    project_assign = project.assigned_users.filter(full_name__exact=request.user.full_name)
    project_assign1 = project.project_lead.filter(full_name__exact=request.user.full_name)
    assigned_table = AssignedCard(assigned)
    form = TicketAssignForm(request.POST or None, instance=issue)
    form.fields["assigned_users"].queryset = CustomUser.objects.filter(Q(project_lead=project) | Q(assigned_users=project)).distinct()
    form1 = TicketEditForm(request.POST or None, instance=issue)
    fixed_date = issue.issue_date_complete
    spcform = SpcTicketForm(request.POST or None, instance=issue)

    if 'assign_self' in request.POST:
        issue_assign = issue
        issue_assign.assigned_users.add(request.user)
        issue_assign.issue_fixed = 'In Progress'
        issue_assign.save()
        return redirect('ticket_page', ticket_id)

    if 'save_user' in request.POST:
        if form.is_valid():
            form.save()
            return redirect('ticket_page', ticket_id)

    if 'edit_ticket' in request.POST:
        if form1.is_valid():
            progress = request.POST.get('issue_fixed')
            if progress == "Fixed":
                fixed_by = form1.save(commit=False)
                fixed_by.fixed_by = request.user
                fixed_by.issue_date_complete = date.today()
                fixed_by.save()
            elif progress == "Closed":
                if issue.issue_date_complete == "":
                    closed_by = form1.save(commit=False)
                    closed_by.closed_by = request.user
                    closed_by.closed_date = date.today()
                    closed_by.save()
                else:
                    closed_by = form1.save(commit=False)
                    closed_by.issue_date_complete = fixed_date
                    closed_by.closed_by = request.user
                    closed_by.closed_date = date.today()
                    closed_by.save()
            else:
                form1.save()
            return redirect('ticket_page', ticket_id)

    context = {
        'ticket_id': ticket_id,
        'issue': issue,
        'assigned_table': assigned_table,
        'user_groups': user_groups,
        'submitter': submitter,
        'assigned1': assigned1,
        'assigned2': assigned2,
        'form': form,
        'form1': form1,
        'spcform': spcform
    }

    if not assigned1:
        issue.issue_fixed = 'Open'
        issue.save()

    if project_assign or project_assign1:
        return render(request, 'bugs/ticket_page.html', context)
    elif admin:
        return render(request, 'bugs/ticket_page.html', context)
    else:
        return redirect('issues')


