from django.shortcuts import render
from markdown import markdown
from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required(login_url='login')
def home(request):
    with open('README.md', 'r', encoding='UTF-8')as f:
        content = f.read()
    return render(request, 'base.html', {'content': content})

def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = User.objects.get(username=request.POST.get('username'))
                messages.success(request, f'Account created for {form.cleaned_data.get("username")}')
                return redirect('login')
        return render(request, 'users/register.html', {'form': form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = AuthenticationForm()
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                login(request, form.user_cache)
                return redirect('home')
        return render(request, 'users/login.html', {'form': form})

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')

def about(request):
    return render(request, 'users/about.html')