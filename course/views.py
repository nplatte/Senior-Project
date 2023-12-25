from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime
from course.models import Course, Student
from course.forms import CourseModelFileForm, EditCourseForm
from django.contrib.auth.decorators import login_required
from teacher_view.models import Assignment


def get_staff_classes(user):
    terms = find_terms()
    current_courses = Course.objects.filter(instructor=user, term__in=terms)
    return current_courses

def find_terms():
    today = datetime.now()
    year = today.year
    month = today.month
    if month < 7:
        terms = [f'{year-1} Fall Term', f'{year} Winter Term', f'{year} May Term']
        return terms
    elif month > 6:
        terms = [f'{year} Fall Term', f'{year+1} Winter Term', f'{year+1} May Term']
        return terms


@login_required()
def edit_course_page(request, course_id):
    current_classes = get_staff_classes(request.user)
    course = Course.objects.get(pk=course_id)
    if request.method == 'POST':
        form = EditCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect(reverse('staff_course_page', kwargs={'course_id': course.pk}))
    return render(request, 'teacher_view/course/edit.html', {
        'current_courses': current_classes,
        'course': course,
        'edit_form': EditCourseForm(instance=course)
    })

@login_required()
def add_course_page(request):
    current_classes = get_staff_classes(request.user)
    if request.method == 'POST':
        file_form = CourseModelFileForm(request.POST, request.FILES)
        if file_form.is_valid():
            new_course = file_form.save()
            return redirect(course_page, course_id=new_course.pk)
    else:
        file_form = CourseModelFileForm()
    return render(request, 'teacher_view/course/create.html', 
    {'current_courses' : current_classes,
     'file_form': file_form
        })

def courses_page(request):
    all_staff_courses = Course.objects.filter(instructor=request.user)
    current_courses = get_staff_classes(request.user)
    return render(request, 'teacher_view/course/courses.html', {
        'all_courses': all_staff_courses,
        'current_courses': current_courses
    })

def course_page(request, course_id):
    current_classes = get_staff_classes(request.user)
    current_course = Course.objects.get(pk=int(course_id))
    if request.POST.get('submit',):
        new_student = Student.objects.get(number=request.POST.get('student_id')) 
        current_course.students.add(new_student)
        current_course.save()
    elif request.POST.get('delete',):
        deleted_student = Student.objects.get(number=request.POST.get('student_id'))
        current_course.students.remove(deleted_student)
        current_course.save()
    assignments =  Assignment.objects.filter(
        course=current_course, 
        ).order_by('-due_date').reverse()
    course_students = Student.objects.filter(enrolled_students=current_course)
    return render(request, 'teacher_view/course/view.html', 
    {'current_courses' : current_classes,
    'current_course' : current_course,
    'assignments': assignments,
    'students' : course_students,
        })

