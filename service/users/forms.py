from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']
