from teacher_view import views as teacher_views
from django.conf.urls import url
from django.urls import path

urlpatterns = [
    url(r'accounts/profile', teacher_views.profile_page, name = 'teacher profile')
]