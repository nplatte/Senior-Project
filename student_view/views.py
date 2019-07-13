from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    return render(request, 'home.html')

def profile_page(request):
    return render(request, 'student_profile.html')
