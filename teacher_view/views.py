from django.shortcuts import render
from Class.models import Course, Assignment
from datetime import date, timedelta, timezone


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
    current_course = current_classes.get(title=course_title)
    new_assignments =  Assignment.objects.filter(
        course=current_course, 
        due_date__gte=date.today()
        ).order_by('-due_date').reverse()
    past_assignments =  Assignment.objects.filter(
        course=current_course, 
        due_date__lte=date.today()
        ).order_by('-due_date').reverse()
    return render(request, 'teacher_view/course_page.html', 
    {'current_courses' : current_classes,
    'current_course' : current_course,
    'upcoming_assignments' : new_assignments,
    'past_assignments' : past_assignments
        })

def past_courses_page(request):
    current_classes = get_staff_classes(request.user)
    return render(request, 'teacher_view/past_courses.html', 
    {'current_courses' : current_classes,
        })

def get_staff_classes(user):
    user_courses = Course.objects.filter(course_instructor=user)
    return user_courses