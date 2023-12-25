from assignment import views as assignment_views
from django.urls import path

urlpatterns = [
    path('<course_id>/add', assignment_views.add_assignment_page, name='add_assignment_page'),
    path('<assignment_id>/edit', assignment_views.edit_assignment_page, name='edit_assignment_page') 
]