from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-style'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-style'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-style'}))

    class Meta:
        model = CustomUser
        fields =('first_name', 'last_name', 'email', 'password1', 'password2')
        help_texts = {'email': None,}

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = ""
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['first_name'].label = ""
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].label = ""
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['password1'].widget.attrs['class'] = 'form-style'
        self.fields['password1'].label = ""
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].help_text = None
        self.fields['password2'].widget.attrs['class'] = 'form-style'
        self.fields['password2'].label = ""
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].help_text = None

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")