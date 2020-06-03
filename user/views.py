from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required(login_url='login')
def home(request):
    return render(request, 'base.html')

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
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        return render(request, 'users/login.html')

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')