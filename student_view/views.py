from django.shortcuts import render
from django.http import HttpResponse
from Class.models import Course

def home_page(request):
    return render(request, 'home.html')

def profile_page(request):
    current_user = request.user
    #print('\n' + current_user.first_name + current_user.last_name + '\n')
    course_list = Course.objects.filter(
        students__name=current_user.first_name + ' ' + current_user.last_name
        )
    some_class = course_list.first()
    return render(
        request, 
        'student_profile.html', 
        { 
        'user': current_user , 
        'student_courses': course_list ,
        }
        )
