from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


# Create your views here.

def index(request):
    if not request.user.is_authenticated or not request.user.is_superuser or not request.user.is_staff:
        return HttpResponseRedirect(reverse('admin-login'))
    data = dict()
    data['user'] = request.user
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('admin-login'))
    return render(request, 'admin/index.html', data)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('admin-login'))


def login_view(request):
    if request.method == "GET":
        data = dict()
        if request.user.is_authenticated:
            if request.user.is_superuser and request.user.is_staff:
                return HttpResponseRedirect(reverse('admin-index'))

            return render(request, 'admin/login.html', {"error": "شما این دسترسی را ندارید"})
        return render(request, 'admin/login.html', data)
    if request.method == "POST":
        uName = request.POST.get("username", None)
        password = request.POST.get("password", None)
        user = authenticate(request, username=uName, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('admin-index'))
        else:
            return render(request, 'admin/login.html', {"error": "نام کاربری یا کلمه عبور اشتباه است"})
