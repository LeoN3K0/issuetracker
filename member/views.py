from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from .models import CustomUser, AccessRequest
from .forms import UserPasswordResetForm, RequestAccessForm, UpdateUserForm, UpdateProfileForm
from .decorators import unauthenticated_user
from bugtracker.models import Project, Issue
from bugtracker.tables import SubmittedTickets, AssignedTickets, ProjectsList
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from datetime import date, datetime
from .tables import RequestTable
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

@method_decorator(unauthenticated_user, name='get')
@method_decorator(unauthenticated_user, name='post')
class login_register(View):
    def get(self, request):
        form = RequestAccessForm()
        if "sign-in" in request.GET:
            username = request.GET.get("username")
            password = request.GET.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('bugtracker')
            else:
                messages.info(request, 'Login attempt failed.')
                return redirect('login_register')
        elif "demo-admin" in request.GET:
            username = "demo_admin@demo.com"
            password = "testuser"
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('bugtracker')
        elif "demo-leader" in request.GET:
            username = "demo_leader@demo.com"
            password = "testuser"
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('bugtracker')
        elif "demo-user" in request.GET:
            username = "demo_user@demo.com"
            password = "testuser"
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('bugtracker')
        return render(request, 'members/login_register.html', {'form': form, 'using_backcard': request.session.pop('using_backcard', False)})

    def post(self, request):
        admin = CustomUser.objects.get(email='emalberg@live.com')
        if "sign-up" in request.POST:
            form = RequestAccessForm(request.POST)
            request.session['using_backcard'] = True
            if form.is_valid():
                cd = form.save(commit=False)
                cd.request_date = datetime.now()
                cd.save()
                ab = form.cleaned_data
                subject = "Bug Tracker: Access Requested"
                email_template_name = "members/request_access.txt"
                c = {
                    "email": admin.email,
                    'domain': 'emalberg.pythonanywhere.com',
                    'site_name': 'emalberg.pythonanywhere.com',
                    "first_name": ab.get('first_name'),
                    "last_name": ab.get('last_name'),
                    "request_email": ab.get('email'),
                    "reason": ab.get('reason'),
                    'protocol': 'https',
                }
                email = render_to_string(email_template_name, c)
                messages.success(request, 'Request Email has been sent, please give up to 24hrs before requesting again.')
                try:
                    send_mail(subject, email, 'erich.malberg@gmail.com', [admin.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return redirect('login_register')

            else:
                messages.error(request, form.errors)
                return redirect('login_register')

        return render(request, 'login_register.html')


def logout_user(request):
    logout(request)
    messages.success(request, ("You were logged out!"))
    return redirect('login_register')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = UserPasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = CustomUser.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "members/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'emalberg.pythonanywhere.com',
                    'site_name': 'emalberg.pythonanywhere.com/bugtracker/',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'https',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'erich.malberg@gmail.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = UserPasswordResetForm()
    return render(request=request, template_name="members/password_reset.html", context={"password_reset_form": password_reset_form})


@login_required(login_url='login_register')
def profile_request(request, full_name):
    user = request.user
    admin = user.groups.filter(name="Admin")
    group = user.groups.values_list('name', flat=True)
    grouplist = group[0]
    if not admin:
        projectlist = Project.objects.filter(Q(project_lead=user) | Q(assigned_users=user)).distinct()
        submittedticket = Issue.objects.filter(submitter=user)
        assignedticket = Issue.objects.filter(assigned_users=user)
    else:
        projectlist = Project.objects.all()
        submittedticket = Issue.objects.filter(issue_fixed="Closed")
        assignedticket = Issue.objects.filter(issue_fixed="Open")

    subtickets = SubmittedTickets(submittedticket)
    atickets = AssignedTickets(assignedticket)
    projects = ProjectsList(projectlist)
    context = {
        'group': grouplist,
        'user': user,
        'full_name': full_name,
        'submitted': subtickets,
        'assigned': atickets,
        'projects': projects,
        'admin': admin,

    }

    return render(request, 'members/profile.html', context)

@login_required(login_url='login_register')
def editprofile_request(request, full_name):
    user = request.user
    admin = user.groups.filter(name="Admin")
    group = user.groups.values_list('name', flat=True)
    grouplist = group[0]

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile', user.full_name)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    context = {
        'group': grouplist,
        'user': user,
        'full_name': full_name,
        'admin': admin,
        'user_form': user_form,
        'profile_form': profile_form,

    }

    return render(request, 'members/editprofile.html', context)

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'members/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('bugtracker')


def requested_access(request):
    table = RequestTable(AccessRequest.objects.all())
    admin = request.user.groups.filter(name__exact='Admin')
    if not admin:
        return redirect('bugtracker')
    return render(request, 'members/accessrequest.html', {'table': table})

@login_required(login_url='login_register')
def deny_access(request, email):
    requester = get_object_or_404(AccessRequest, email=email)
    subject = "Bug Tracker: Access Denied"
    email_template_name = "members/access_denied.txt"
    c = {
        "email": requester.email,
        'domain': 'emalberg.pythonanywhere.com',
        'site_name': 'emalberg.pythonanywhere.com/bugtracker/',
        "first_name": requester.first_name,
        "last_name": requester.last_name,
        'protocol': 'https',
    }
    email = render_to_string(email_template_name, c)
    try:
        send_mail(subject, email, 'erich.malberg@gmail.com', [requester.email], fail_silently=False)
        requester.delete()
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    return redirect('access_request')

@login_required(login_url='login_register')
def accept_access(request, email):
    requester = get_object_or_404(AccessRequest, email=email)
    subject = "Bug Tracker: Access Accepted"
    email_template_name = "members/access_accepted.txt"
    username = f'{requester.first_name}.{requester.last_name}'
    password = f'{requester.first_name}123'
    newuser = get_user_model().objects.create_user(username=username, first_name=requester.first_name, last_name=requester.last_name,
                                                            email=requester.email, password=password)
    user = get_object_or_404(CustomUser, email=email)
    my_group = Group.objects.get(name='General User')
    my_group.user_set.add(user)
    c = {
        "email": requester.email,
        'domain': 'emalberg.pythonanywhere.com',
        'site_name': 'emalberg.pythonanywhere.com/bugtracker/',
        "first_name": requester.first_name,
        "last_name": requester.last_name,
        'token': default_token_generator.make_token(user),
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        'protocol': 'https',
    }
    email = render_to_string(email_template_name, c)
    try:
        send_mail(subject, email, 'erich.malberg@gmail.com', [requester.email], fail_silently=False)
        requester.delete()
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    return redirect('access_request')


