from course import views as course_views
from django.urls import path

urlpatterns = [
    path('all/', course_views.courses_page, name='courses_page'),
    path('add/', course_views.add_course_page, name='add_course_page'),
    path('<course_id>/edit/', course_views.edit_course_page, name='edit_course_page'), 
    path('<course_id>/', course_views.course_page, name='view_course_page'),
    path('<student_id>/all/', course_views.courses_api_page, name='view_courses_api')
]