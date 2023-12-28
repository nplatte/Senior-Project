from django.shortcuts import render, redirect
from django.urls import reverse
from assignment.models import Assignment
from assignment.forms import AssignmentForm
from django.contrib.auth.decorators import login_required
from course.models import Course
from teacher_view.views import get_staff_classes

'''def get_staff_classes(user):
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
        return terms'''

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
        request, 'assignment/create.html',
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
    return render(request, 'assignment/edit.html',
    {'current_courses' : current_classes,
    'assignment' : edit_ass,
    'form': form
    })