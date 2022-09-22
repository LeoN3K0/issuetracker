from django.urls import path
from . import views

urlpatterns = [
    path('bugtracker', views.bugtracker, name='bugtracker'),
    path('projects', views.projects_page, name='projects'),
]