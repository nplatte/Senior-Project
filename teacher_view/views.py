from django.shortcuts import render

def profile_page(request):
    return render(request, "teacher_view/profile.html")

def add_course_page(request):
    return render(request, 'teacher_view/create_class.html')
