from django.urls import path
from . import views
from .views import ChartData

urlpatterns = [
    #index URLS
    path('bugtracker/', views.bugtracker, name='bugtracker'),
    path('api/chart/data/', ChartData.as_view()),
    path('search_ticket/', views.search_site, name='search_site'),

    #Project Model Related URLS
    path('projects/', views.projects_table_page, name='projects'),
    path('projects/add_project/', views.add_project_page, name='add_project',),
    path('projects/<str:name>/', views.project_page, name="project_page"),
    path('delete_project/<str:name>', views.delete_project, name="delete_project"),
    path('update_project/<str:name>', views.update_project, name="update_project"),

    #Issue Model Related URLS
    path('issues/', views.issues_table_page, name='issues'),
    path('issues/submit_ticket/', views.submit_ticket_page, name='submit_ticket',),
    path('issues/<str:ticket_id>/', views.ticket_page, name="ticket_page"),
]