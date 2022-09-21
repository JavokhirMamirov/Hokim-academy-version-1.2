from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.status == 1:
                login(request, user)
                return redirect('admin-dashboard')
            elif user.status == 2:
                login(request, user)
                return redirect('organ-dashboard')
            elif user.status == 3:
                login(request, user)
                return redirect('school-dashboard')
            else:
                messages.error(request, 'Username yoki Parol xato!')
                return redirect('admin-login')
        else:
            messages.error(request, 'Username yoki Parol xato!')
            return redirect('admin-login')
    if request.user.is_authenticated:
        if request.user.status == 2:
            return redirect('organ-dashboard')
        elif request.user.status == 3:
            return redirect('school-dashboard')
        else:
            admin_logout()
    return render(request, 'auth/signin.html')


def admin_logout(request):
    logout(request)
    return redirect('admin-login')

def page_404(request):
    return render(request, 'auth/page_404.html')
