from django.contrib.auth import authenticate, login as mylogin, logout as mylogout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import UserCreationForm

# Create your views here.


def index(request):
    if str(request.user) == 'AnonymousUser':
        return HttpResponseRedirect(reverse('authentication:login'))
    else:
        return render(request, 'authentication/index.html')


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('authentication:index'))
    else:
        if request.method == 'GET':
            template = 'authentication/login.html'
            return render(request, template)
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                mylogin(request, user)
                return HttpResponseRedirect(reverse('authentication:index'))
            else:
                return render(request, "authentication/invalidlogin.html")


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('authentication:index'))
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(request, username=username, password=raw_password)
                mylogin(request, user)
                return HttpResponseRedirect(reverse('authentication:index'))
        else:
            form = UserCreationForm()
        return render(request, 'authentication/signup.html', {'form': form})


def logout(request):
    mylogout(request)
    return HttpResponseRedirect(reverse('authentication:login'))
