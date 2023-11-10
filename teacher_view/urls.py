from teacher_view import views as teacher_views
from django.urls import path

urlpatterns = [
    path('', teacher_views.home_page, name='staff_home_page'),
    path('accounts/profile', teacher_views.profile_page, name='staff_profile_page'),
    path('course/', teacher_views.courses_page, name='staff_courses_page'),
    path('course/add', teacher_views.add_course_page, name='staff_add_course_page'),
    path('course/<course_title>/grade', teacher_views.grade_course_page, name='course_grade_page'),
    path('course/<course_id>/', teacher_views.course_page, name='staff_course_page'),
    path('course/previous/<course_title>-<term>/', teacher_views.past_course_page, name='past_course_page'),
    path('course/previous', teacher_views.past_courses_page, name='past_courses_page'),
    path('assignment/<course_title>/add', teacher_views.add_assignment_page, name='create_assignment'),
    path('assignment/<assignment_title>/edit', teacher_views.edit_assignment_page, name='edit_assignment'),
    
]