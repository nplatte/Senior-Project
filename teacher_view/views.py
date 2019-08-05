from django.shortcuts import render

def profile_page(request):
    return render(request, "teacher_view/profile.html")
