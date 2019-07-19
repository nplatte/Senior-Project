from django.shortcuts import render
from django.http import HttpResponse
from Class.models import Course, Assignment
from datetime import date

def home_page(request):
    return render(request, 'home.html', )

def profile_page(request):
    current_user = request.user
    course_list = _get_course_list(request)
    assignments = Assignment.objects.filter(
            course__in=course_list, 
            due_date__gte=date.today()
            ).order_by('-due_date').reverse()
    return render(
        request, 
        'student_profile.html', 
        { 
        'user': current_user , 
        'student_courses': course_list ,
        'course_assignments': assignments,
        }
        )

def assignment_page(request, assignment_title):
    course_list = _get_course_list(request)
    current_assignment = Assignment.objects.get(title=assignment_title)
    return render(request, 'assignment.html', {'assignment':current_assignment, 'student_courses': course_list})

def course_page(request, course_title):
    course_list = _get_course_list(request)
    current_course = Course.objects.get(title=course_title)
    course_assignments = Assignment.objects.filter(course = current_course)
    return render(
        request, 
        'course.html', 
        {'course':current_course,
        'student_courses': course_list,
        'courses_assignments': course_assignments
        })

def grade_page(request):
    course_list = _get_course_list(request)
    return render(request, 'grades.html', {'student_courses': course_list})

def handout_page(request):
    course_list = _get_course_list(request)
    return render(request, 'handouts.html', {'student_courses': course_list})

def discussion_page(request):
    course_list = _get_course_list(request)
    return render(request, 'discussion.html', {'student_courses': course_list})

def _get_course_list(request):
    current_user = request.user
    course_list = Course.objects.filter(
        students__name=current_user.first_name + ' ' + current_user.last_name
        )
    return course_list