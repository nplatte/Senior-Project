from teacher_view import views as teacher_views
from django.urls import path

urlpatterns = [
    path('', teacher_views.HomePageView.as_view(), name='staff_home_page'),
    path('accounts/profile', teacher_views.ProfilePageView.as_view(), name='staff_profile_page'),   
]