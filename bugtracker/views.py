from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from.models import Project


@login_required(login_url='login_register')
def bugtracker(request):
    project_card_list = Project.objects.all()
    return render(request, 'main_index.html', {'project_card_list': project_card_list})


@login_required(login_url='login_register')
def projects_page(request):
    project_card_list = Project.objects.all()
    return render(request, 'projects.html', {'project_card_list': project_card_list})