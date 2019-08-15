"""superlists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from .views import *
from django.urls import path


urlpatterns = [
    url(r'accounts/', include('django.contrib.auth.urls')),
    path('assignment/<assignment_title>/', assignment_page, name='view_assignment'),
    path('course/<course_title>/', course_page, name='view_course'),
    path('course/previous', past_courses_page, name='view_past_courses'),
    path('course/previous/<course_title>-<term>/', past_course_page, name='past_course_page'),
    path('grades/', grade_page, name='view_grades'),
    path('handouts/', handout_page, name='view_handouts'),
    path('discussion/', discussion_page, name='view_discussion'),
    path('handout/<handout_title>/', handout_page, name='view_handout'),
]