from django.shortcuts import render, redirect
from django.urls import reverse
from teacher_view.models import Assignment
from .models import Grade
from datetime import date
from teacher_view.forms import AssignmentForm
from django.contrib.auth.decorators import login_required
from django import views
from django.utils.decorators import method_decorator
from course.models import Course, Student


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
    common_timezones = {
            "Chicago": "America/Chicago",
            "New York": "America/New_York"
        }
    

    def get(self, request, *args, **kwargs):
        current_classes = get_staff_classes(request.user)
        return render(request, self.template, {"timezones": self.common_timezones, 'current_courses': current_classes})

    def post(self, request, *args, **kwargs):
        current_classes = get_staff_classes(request.user)
        request.session["django_timezone"] = request.POST["timezone"]
        return render(request, self.template, {"timezones": self.common_timezones, 'current_courses': current_classes})

    

class ProfilePageView(TeacherView):

    template = "teacher_view/profile.html"



def add_assignment_page(request, course_id):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            c = Course.objects.get(pk=course_id)
            return redirect(c.get_absolute_url(), course_id=course_id)
    form = AssignmentForm()
    current_classes = get_staff_classes(request.user)
    context = {
        'current_courses': current_classes,
        'assignment_form': form
    }
    return render(
        request, 'teacher_view/assignment/create.html',
        context
    )

@login_required()
def edit_assignment_page(request, assignment_id):
    edit_ass = Assignment.objects.get(pk=assignment_id)
    current_classes = get_staff_classes(request.user)
    form = AssignmentForm(instance=edit_ass)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=edit_ass)
        if form.is_valid():
            form.save()
            return redirect(reverse('view_course_page', kwargs={'course_id':edit_ass.course.pk}))
    return render(request, 'teacher_view/assignment/edit.html',
    {'current_courses' : current_classes,
    'assignment' : edit_ass,
    'form': form
    })

def get_staff_classes(user):
    terms = find_terms()
    current_courses = Course.objects.filter(instructor=user, term__in=terms)
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

def get_all_past_terms(request):
    terms = find_terms()
    user_courses = Course.objects.filter(instructor=request.user).exclude(term__in=terms).values('term')
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