from django.shortcuts import render, redirect
from django.urls import reverse
from teacher_view.models import Course, Assignment, Student
from .models import Grade
from datetime import date
from teacher_view.forms import CourseModelFileForm, EditCourseForm, AssignmentForm
from django.contrib.auth.decorators import login_required
from django import views
from django.utils.decorators import method_decorator


@method_decorator(login_required, 'dispatch')
class TeacherView(views.View):

    template = ''

    def get(self, request):
        current_classes = get_staff_classes(request.user)
        return render(request, self.template, {
            'current_courses': current_classes
        })


class HomePageView(TeacherView):

    template = 'teacher_view/home.html'
    

class ProfilePageView(TeacherView):

    template = "teacher_view/profile.html"


@login_required()
def edit_course_page(request, course_id):
    current_classes = get_staff_classes(request.user)
    course = Course.objects.get(pk=course_id)
    if request.method == 'POST':
        form = EditCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect(reverse('staff_course_page', kwargs={'course_id': course.pk}))
    return render(request, 'teacher_view/edit_course.html', {
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
    return render(request, 'teacher_view/create_class.html', 
    {'current_courses' : current_classes,
     'file_form': file_form
        })

def courses_page(request):
    return render(request, 'teacher_view/courses.html')

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
    return render(request, 'teacher_view/course_page.html', 
    {'current_courses' : current_classes,
    'current_course' : current_course,
    'assignments': assignments,
    'students' : course_students,
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

def add_assignment_page(request, course_id):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(course_page, course_id=course_id)
    form = AssignmentForm()
    current_classes = get_staff_classes(request.user)
    context = {
        'current_courses': current_classes,
        'assignment_form': form
    }
    return render(
        request, 'teacher_view/add_assignment.html',
        context
    )

def edit_assignment_page(request, assignment_id):
    editable_assignment = Assignment.objects.get(pk=assignment_id)
    current_classes = get_staff_classes(request.user)
    if request.POST.get('submit',):
        _edit_assignment(request, editable_assignment)
    elif request.POST.get('delete',):
        editable_assignment.delete()
        return render(request, "teacher_view/profile.html", {'current_courses' : current_classes,})
    return render(request, 'teacher_view/edit_assignment.html',
    {'current_courses' : current_classes,
    'assignment' : editable_assignment
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
    return content_list[:-1]