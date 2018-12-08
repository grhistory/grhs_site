from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout, authenticate, login as django_login

def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            next = request.POST.get("next", "/")
            return redirect(next)
        else:
            return render(request, "membership/login.html", {"next": request.POST.get("next", "/"), "username": username, "errors": "yes"})
    else:
        return render(request, "membership/login.html", {"next": request.GET.get("next", "/")})

def logout(request):
    django_logout(request)
    next = request.GET.get("next", "/")
    return redirect(next)