from django.shortcuts import render

def profile_page(request):
    return render(request, "teacher_view/profile.html")

def add_course_page(request):
    return render(request, 'teacher_view/create_class.html')

def course_page(request, course_title):
    return render(request, 'teacher_view/course_page.html')
