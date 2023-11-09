from django.shortcuts import render
from teacher_view.models import Course, Assignment, Student
from student_view.models import HomeworkSubmission
from .models import Grade
from datetime import date, timedelta, timezone
from time import sleep
from teacher_view.forms import CourseModelForm
from django.contrib.auth.decorators import login_required

@login_required()
def home_page(request):
    current_classes = get_staff_classes(request.user)
    return render(request, 'teacher_view/home.html', 
    {'current_courses' : current_classes,
        })

@login_required()
def profile_page(request):
    current_classes = get_staff_classes(request.user)
    return render(request, "teacher_view/profile.html", 
    {'current_courses' : current_classes,
        })

@login_required
def add_course_page(request):
    current_classes = get_staff_classes(request.user)
    
    if request.method == 'POST':
        _create_course(request)
    else:
        file_form = CourseModelForm()
    return render(request, 'teacher_view/create_class.html', 
    {'current_courses' : current_classes,
     'file_form': file_form
        })

def courses_page(request):
    return render(request, 'teacher_view/courses.html')

def course_page(request, course_title):
    current_classes = get_staff_classes(request.user)
    current_course = current_classes.get(title=course_title)
    if request.POST.get('submit',):
        new_student = Student.objects.get(number=request.POST.get('student_id'))
        current_course.students.add(new_student)
        current_course.save()
    elif request.POST.get('delete',):
        deleted_student = Student.objects.get(number=request.POST.get('student_id'))
        current_course.students.remove(deleted_student)
        current_course.save()
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

def past_course_page(request, course_title, term):
    current_classes = get_staff_classes(request.user)
    current_course = Course.objects.get(title=course_title, term=term)
    new_assignments =  Assignment.objects.filter(
        course=current_course, 
        due_date__gte=date.today()
        ).order_by('-due_date').reverse()
    past_assignments =  Assignment.objects.filter(
        course=current_course, 
        due_date__lt=date.today()
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
    past_courses = [Course.objects.filter(term=term, course_instructor=request.user) for term in terms]
    return render(request, 'teacher_view/past_courses.html', 
    {'current_courses' : current_classes,
    'past_courses' : past_courses
        })

def grade_course_page(request, course_title):
    if request.method == 'POST':
        update_grades(request, course_title)
    current_classes = get_staff_classes(request.user)
    current_course = current_classes.get(title=course_title)
    course_grades = Grade.objects.filter(course=current_course)
    return render(request, 'teacher_view/grade_course.html',
    {'current_courses' : current_classes,
    'student_grades' : course_grades, 
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
    terms = find_terms()
    current_courses = Course.objects.filter(course_instructor=user, term__in=terms)
    return current_courses

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
    terms = find_terms()
    user_courses = Course.objects.filter(course_instructor=request.user).exclude(term__in=terms).values('term')
    past_terms = set( val for dic in user_courses for val in dic.values())
    return past_terms

def update_grades(request, title):
    terms = find_terms()
    current_course = Course.objects.get(title=title, term__in=terms)
    parsed_file = parse_grade_file(request.FILES["grade_file"])
    for grade_object in Grade.objects.filter(course=current_course):
        grade_object.delete()
    for grade_set in parsed_file[1:-2]:
        new_grade = Grade()
        new_grade.student = Student.objects.get(number=grade_set[0])
        tab = '   '
        new_grade.student_scores = tab.join(grade_set)[:-2]
        new_grade.course = current_course
        new_grade.catagories = tab.join(parsed_file[0])[:-2]
        new_grade.points_possible = tab.join(parsed_file[-1])[:-3]
        new_grade.letter_grade = grade_set[-1][:-2]
        new_grade.save()

def parse_grade_file(file):
    content_list = str(file.read()).split('\\n')
    content_list = [group.split('\\t') for group in content_list]
    char_remove = ['','b"', ' ']
    for group in content_list:
        for entry in group:
            if entry in char_remove:
                group.remove(entry)
        print(group)
    return content_list[:-1]