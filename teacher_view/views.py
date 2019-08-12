from django.shortcuts import render
from Class.models import Course, Assignment, Student
from student_view.models import HomeworkSubmission
from datetime import date, timedelta, timezone
from time import sleep


def profile_page(request):
    current_classes = get_staff_classes(request.user)
    return render(request, "teacher_view/profile.html", 
    {'current_courses' : current_classes,
        })

def add_course_page(request):
    current_classes = get_staff_classes(request.user)
    if request.method == 'POST':
        _create_course(request)
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
    course_students = Student.objects.filter(enrolled_students=current_course)
    return render(request, 'teacher_view/course_page.html', 
    {'current_courses' : current_classes,
    'current_course' : current_course,
    'upcoming_assignments' : new_assignments,
    'past_assignments' : past_assignments,
    'students' : course_students,
        })

def past_courses_page(request):
    current_classes = get_staff_classes(request.user)
    terms = get_all_past_terms(request)
    past_courses = [Course.objects.filter(term=term) for term in terms]
    print(past_courses)
    return render(request, 'teacher_view/past_courses.html', 
    {'current_courses' : current_classes,
    'past_courses' : past_courses
        })

def add_assignment_page(request, course_title):
    if request.method == 'POST':
        _create_assignment(request, course_title)
    current_classes = get_staff_classes(request.user)
    return render(request, 'teacher_view/create_assignment.html',
    {'current_courses' : current_classes,
    })

def edit_assignment_page(request, assignment_title):
    editable_assignment = Assignment.objects.get(instructor=request.user, title=assignment_title)
    current_classes = get_staff_classes(request.user)
    assignment_homework = HomeworkSubmission.objects.filter(assignment=editable_assignment)
    if request.POST.get('submit',):
        _edit_assignment(request, editable_assignment)
    elif request.POST.get('delete',):
        editable_assignment.delete()
        return render(request, "teacher_view/profile.html", {'current_courses' : current_classes,})
    return render(request, 'teacher_view/edit_assignment.html',
    {'current_courses' : current_classes,
    'assignment' : editable_assignment,
    'student_homework' : assignment_homework,
    })

def get_staff_classes(user):
    today = date.today()
    year = today.year
    month = today.month
    terms = find_terms(month, year)
    current_courses = Course.objects.filter(course_instructor=user, term__in=terms)
    return current_courses
    

def find_terms(month, year):
    if month < 7:
        terms = [f'{year-1} Fall Term', f'{year} Winter Term', f'{year} May Term']
        return terms
    elif month > 6:
        terms = [f'{year} Fall Term', f'{year+1} Winter Term', f'{year+1} May Term']
        return terms

def _create_course(request):
    new_course = Course()
    new_course.Class_File = request.FILES["class_file"]
    new_course.save()
    new_course.course_instructor = request.user
    new_course.create()

def _create_assignment(request, course_title):
    new_assignment = Assignment()
    new_assignment.title = request.POST['title']
    new_assignment.description = request.POST['description']
    new_assignment.due_date = request.POST['due_date']
    new_assignment.course = get_staff_classes(request.user).get(title=course_title)
    new_assignment.instructor = request.user
    new_assignment.save()

def _edit_assignment(request, assignment):
    assignment.title = request.POST['title']
    assignment.description = request.POST['description']
    assignment.due_date = request.POST['due_date']
    assignment.save()

def get_all_past_terms(request):
    today = date.today()
    year = today.year
    month = today.month
    terms = find_terms(month, year)
    user_courses = Course.objects.filter(course_instructor=request.user).exclude(term__in=terms).values('term')
    past_terms = set( val for dic in user_courses for val in dic.values())
    return past_terms
    


