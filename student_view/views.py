from django.shortcuts import render
from django.http import HttpResponse
from Class.models import Course, Assignment

def home_page(request):
    return render(request, 'home.html')

def profile_page(request):
    current_user = request.user
    course_list = Course.objects.filter(
        students__name=current_user.first_name + ' ' + current_user.last_name
        )
    assignments = Assignment.objects.filter(course__in=course_list).order_by('-due_date')
    return render(
        request, 
        'student_profile.html', 
        { 
        'user': current_user , 
        'student_courses': course_list ,
        'course_assignments': assignments,
        }
        )

def view_assignment(request, assignment_title):
    current_assignment = Assignment.objects.get(title=assignment_title)
    return render(request, 'assignment.html', {'assignment':current_assignment})
