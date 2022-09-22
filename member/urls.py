from django.urls import path
from .views import login_register

from . import views

urlpatterns = [
    path('', login_register.as_view(), name='login_register'),
    path('logout_user', views.logout_user, name='logout_user'),
]