from django.test import TestCase
from django.urls import resolve
from django.http import HttpResponse
from django.template.loader import render_to_string

from .views import home_page, course_page


