from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator


from .decorators import unauthenticated_user
from .forms import RegisterUserForm

@method_decorator(unauthenticated_user, name='get')
@method_decorator(unauthenticated_user, name='post')
class login_register(View):


    def get(self, request):
        form = RegisterUserForm()
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
        return render(request, 'login_register.html', {'form': form, 'using_backcard': request.session.pop('using_backcard', False)})

    def post(self, request):
        if "sign-up" in request.POST:
            form = RegisterUserForm(request.POST)
            request.session['using_backcard'] = True
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account has been created succesfully')
                return redirect('login_register')
            else:
                messages.error(request, form.errors)
                return redirect('login_register')

        return render(request, 'login_register.html')

def logout_user(request):
    logout(request)
    messages.success(request, ("You were logged out!"))
    return redirect('login_register')