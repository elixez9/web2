from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.forms import User
from django.contrib.auth import authenticate, login, logout


class RegisterView(View):
    form_class = UserRegistrationForm

    def get(self, request):
        form = self.form_class
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('<PASSWORD>')
            email = form.cleaned_data.get('email')
            User.objects.create_user(username=username, password=password, email=email)
            messages.success(request, 'Account was created for ' + username)
            return redirect('home')
        return render(request, 'account/register.html', {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm

    def get(self, request):
        form = self.form_class
        return render(request, 'account/login.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are now logged in')
                return redirect('home')
            messages.error(request, 'Invalid username or password')
        return render(request, 'account/login.html', {'form': form})


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('home')