from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse

from datetime import datetime

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user.groups.filter(name='staff').exists():
            login(request, user)
            return redirect(reverse('staff_home_page'))
        else:
            return redirect('/')
    return render(request, 'login/login.html')
