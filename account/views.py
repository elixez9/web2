from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.forms import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


class RegisterView(View):
    form_class = UserRegistrationForm

    def dispatch(self, request, *args, **kwargs):  #If the user is logged in, do not show the registration form
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)  #Otherwise, show the registry form

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

    def dispatch(self, request, *args, **kwargs):  #If the user is logged in, do not show the registration form
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)  #Otherwise, show the registry form

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


class UserLogoutView(LoginRequiredMixin, View):    #LoginRequiredMixin class Logout is only shown to logged in users
    def get(self, request):
        logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('home')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        return render(request, 'account/profile.html', {'user': user})
