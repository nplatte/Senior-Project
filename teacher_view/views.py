from django.shortcuts import render
from Class.models import Course

def profile_page(request):
    current_classes = get_staff_classes(request.user)
    return render(request, "teacher_view/profile.html", 
    {'current_courses' : current_classes,
        })

def add_course_page(request):
    current_classes = get_staff_classes(request.user)
    return render(request, 'teacher_view/create_class.html', 
    {'current_courses' : current_classes,
        })

def course_page(request, course_title):
    current_classes = get_staff_classes(request.user)
    return render(request, 'teacher_view/course_page.html', 
    {'current_courses' : current_classes,
        })

def past_courses_page(request):
    current_classes = get_staff_classes(request.user)
    return render(request, 'teacher_view/past_courses.html', 
    {'current_courses' : current_classes,
        })

def get_staff_classes(user):
    user_courses = Course.objects.filter(course_instructor=user)
    return user_courses