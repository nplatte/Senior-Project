from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from Class.models import Course, Assignment, Handout, Student
from teacher_view.models import Grade
from .models import HomeworkSubmission
from datetime import date, timedelta, timezone
import teacher_view

def home_page(request):
    return render(request, 'student_view/home.html', )

@login_required(login_url='//login/')
def profile_page(request):
    current_user = request.user
    if current_user.is_staff:
        current_classes = teacher_view.views.get_staff_classes(current_user)
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

@login_required(login_url='/login/')
def assignment_page(request, assignment_title):
    course_list = _get_course_list(request)
    current_assignment = Assignment.objects.get(title=assignment_title)
    if request.method == "POST":
        _create_homework(request, request.user, current_assignment)
    return render(request, 'student_view/assignment.html', {'assignment':current_assignment, 'student_courses': course_list})

@login_required(login_url='/login/')
def course_page(request, course_title):
    course_list = _get_course_list(request)
    current_course = course_list.get(title=course_title)
    course_assignments = Assignment.objects.filter(course = current_course)
    current_student = Student.objects.get(name=request.user.first_name + ' ' + request.user.last_name)
    grade = Grade.objects.get(student=current_student, course=current_course)
    return render(
        request, 
        'student_view/course.html', 
        {'course':current_course,
        'student_courses': course_list,
        'courses_assignments': course_assignments,
        'grade' : grade,
        })

@login_required(login_url='/student/accounts/login/')
def past_course_page(request, course_title, term):
    course_list = _get_course_list(request)
    return render(request, 'teacher_view/home.html',
        {'current_courses' : current_classes,
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
    terms = find_terms()
    course_list = Course.objects.filter(
        students__name=current_user.first_name + ' ' + current_user.last_name,
        term__in=terms
        )
    return course_list

@login_required(login_url='/student/accounts/login/')
def past_courses_page(request):
    course_list = _get_course_list(request)
    terms = get_all_past_terms(request)
    past_courses = [Course.objects.filter(term=term) for term in terms]
    return render(request, 'student_view/past_courses.html', 
    {'student_courses': course_list,
    'past_courses' : past_courses
        })

@login_required(login_url='/student/accounts/login/')
def _create_homework(request, user, assignment):
    new_homework = HomeworkSubmission()
    new_homework.homework = request.FILES["document"]
    new_homework.student = user
    new_homework.course = assignment.course
    new_homework.assignment = assignment
    new_homework.save()

def get_staff_classes(user):
    user_courses = Course.objects.filter(students=user)
    return user_courses

def get_all_past_terms(request):
    terms = find_terms()
    student = Student.objects.get(name=request.user.first_name + ' ' + request.user.last_name)
    user_courses = Course.objects.filter(students=student).exclude(term__in=terms).values('term')
    print(user_courses)
    past_terms = set( val for dic in user_courses for val in dic.values())
    return past_terms

def find_terms():
    today = date.today()
    year = today.year
    month = today.month
    if month < 7:
        terms = [f'{year-1} Fall Term', f'{year} Winter Term', f'{year} May Term']
        return terms
    elif month > 6:
        terms = [f'{year} Fall Term', f'{year+1} Winter Term', f'{year+1} May Term']
        return terms