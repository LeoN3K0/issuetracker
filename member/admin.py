from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, AccessRequest


from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "full_name",]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(AccessRequest)