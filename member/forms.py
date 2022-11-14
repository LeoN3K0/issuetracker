from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from .models import CustomUser, Profile, AccessRequest
from crispy_forms.helper import FormHelper


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'form-style',
        'placeholder': 'Email',
    }))

    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)


class UserSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(UserSetPasswordForm, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'class': 'form-style',
        'placeholder': 'Password',
    }))
    new_password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'class': 'form-style',
        'placeholder': 'Confirm Password',
    }))


class RequestAccessForm(forms.ModelForm):
    class Meta:
        model = AccessRequest
        fields = ('first_name', 'last_name', 'email', 'reason', 'request_date')
        help_texts = {'email': None}
        widgets = {

            'request_date': forms.HiddenInput(),

        }

    def __init__(self, *args, **kwargs):
        super(RequestAccessForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = ""
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].widget.attrs['autocomplete'] = 'off'
        self.fields['email'].widget.attrs['class'] = 'form-style'
        self.fields['first_name'].label = ""
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['first_name'].widget.attrs['class'] = 'form-style'
        self.fields['last_name'].label = ""
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['last_name'].widget.attrs['class'] = 'form-style'
        self.fields['reason'].label = ""
        self.fields['reason'].widget.attrs['placeholder'] = 'Reason for request'
        self.fields['reason'].widget.attrs['cols'] = 20
        self.fields['reason'].widget.attrs['rows'] = 5
        self.fields['reason'].widget.attrs['class'] = 'form-style'



class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': '',
            'last_name': '',
            'email': '',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={"class": "form-control-sm", }),
            'last_name': forms.TextInput(attrs={"class": "form-control-sm", }),
            'email': forms.TextInput(attrs={"class": "form-control-sm", }),
        }



class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        labels = {
            'avatar': '',
        }
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control-file'})
        }