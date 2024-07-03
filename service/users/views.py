from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from allauth.account.auth_backends import AuthenticationBackend
from .forms import UserRegistrationForm, UserLoginForm
from application_service.forms import CandidateProfileForm




def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = CandidateProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
            return redirect(reverse_lazy('submit_application'))
    else:
        user_form = UserRegistrationForm()
        profile_form = CandidateProfileForm()
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy('edit_profile'))
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

