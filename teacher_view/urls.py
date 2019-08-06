from teacher_view import views as teacher_views
from django.conf.urls import url
from django.urls import path

urlpatterns = [
    path('accounts/profile', teacher_views.profile_page, name='staff_profile'),
    path('course/add', teacher_views.add_course_page, name='staff_course_create'),
    path('course/<course_title>/', teacher_views.course_page, name='course_page'),
    path('course/previous', teacher_views.past_courses_page, name='past_course_page'),
    path('assignment/<course_title>/add', teacher_views.add_assignment_page, name='create_assignment'),
    path('assignment/<assignment_title>/edit', teacher_views.edit_assignment_page, name='edit_assignment'),
]