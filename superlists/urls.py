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
#from django.conf.urls import url, include
from django.urls import path, include
from django.contrib import admin
from student_view import urls as student_urls
from teacher_view import urls as teacher_urls
from student_view import views as student_views
from login import views as login_views

urlpatterns = [
    # path('login/', include(login_urls)),
    path('', login_views.login_page, name='login_page'),
    path('admin/', admin.site.urls),
    path(r'student/', include(student_urls)),
    path('teacher/', include(teacher_urls)),
    path(r'accounts/profile', student_views.profile_page, name='student_profile_view')
]
