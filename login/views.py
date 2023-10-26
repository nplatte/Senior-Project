from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse

from datetime import datetime

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if user.groups.filter(name='staff').exists():
                return redirect(reverse('staff_home_page'))
            elif user.groups.filter(name='student').exists():
                return redirect(reverse('student_home_page'))
        else:
            return redirect(login_page)
    return render(request, 'login/login.html')
