from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from Class.models import Course, Assignment, Handout
from .models import HomeworkSubmission
from datetime import date, timedelta, timezone
import teacher_view

def home_page(request):
    return render(request, 'student_view/home.html', )

@login_required(login_url='/student/accounts/login/')
def profile_page(request):
    current_user = request.user
    if current_user.is_staff:
        current_classes = get_staff_classes(current_user)
        return render(request, 'teacher_view/home.html',
        {'current_courses' : current_classes,
        }
        )
        
    course_list = _get_course_list(request)
    assignments = Assignment.objects.filter(
        course__in=course_list, 
        due_date__gte=date.today()
        ).order_by('-due_date').reverse()
    handouts = Handout.objects.filter(
        course__in=course_list,
        post_date__lte=date.today() + timedelta(days=7),
    )
    return render(
        request, 
        'student_view/student_profile.html', 
        { 
        'user': current_user , 
        'student_courses': course_list ,
        'course_assignments': assignments,
        'handouts': handouts
        }
        )

@login_required(login_url='/student/accounts/login/')
def assignment_page(request, assignment_title):
    course_list = _get_course_list(request)
    current_assignment = Assignment.objects.get(title=assignment_title)
    if request.method == "POST":
        _create_homework(request, request.user, current_assignment)
    return render(request, 'student_view/assignment.html', {'assignment':current_assignment, 'student_courses': course_list})

@login_required(login_url='/student/accounts/login/')
def course_page(request, course_title):
    course_list = _get_course_list(request)
    current_course = Course.objects.get(title=course_title)
    course_assignments = Assignment.objects.filter(course = current_course)
    return render(
        request, 
        'student_view/course.html', 
        {'course':current_course,
        'student_courses': course_list,
        'courses_assignments': course_assignments
        })

@login_required(login_url='/student/accounts/login/')
def grade_page(request):
    course_list = _get_course_list(request)
    return render(request, 'student_view/grades.html', {'student_courses': course_list})

@login_required(login_url='/student/accounts/login/')
def handout_page(request):
    course_list = _get_course_list(request)
    return render(request, 'student_view/handouts.html', {'student_courses': course_list})

@login_required(login_url='/student/accounts/login/')
def discussion_page(request):
    course_list = _get_course_list(request)
    return render(request, 'student_view/discussion.html', {'student_courses': course_list})

@login_required(login_url='/student/accounts/login/')
def _get_course_list(request):
    current_user = request.user
    course_list = Course.objects.filter(
        students__name=current_user.first_name + ' ' + current_user.last_name
        )
    return course_list

def _create_homework(request, user, assignment_title):
    new_assignment = HomeworkSubmission()
    new_assignment.homework = request.FILES["document"]
    new_assignment.student = user
    new_assignment.course = assignment_title.course
    new_assignment.save()

def get_staff_classes(user):
    user_courses = Course.objects.filter(course_instructor=user)
    return user_courses