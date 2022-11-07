from django.urls import path
from .views import login_register
from .forms import UserPasswordResetForm
from . import views
from .views import ChangePasswordView

urlpatterns = [
    path('', login_register.as_view(), name='login_register'),
    path('logout_user', views.logout_user, name='logout_user'),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('profile/<str:full_name>', views.profile_request, name='profile'),
    path('profile/edit/<str:full_name>', views.editprofile_request, name='edit_profile'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    path('requested_access/',  views.requested_access, name='access_request'),
    path('deny_access/<str:email>', views.deny_access, name="deny_access"),
    path('accept_access/<str:email>', views.accept_access, name="accept_access"),
]