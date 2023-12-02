from django.test import TestCase
from django.urls import resolve
from django.http import HttpResponse
from django.template.loader import render_to_string

from .views import home_page, course_page


class HomePageTest(TestCase):

    def test_root_url(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

class CoursePageTest(TestCase):

    def setUp(self):
        pass

    def test_course_title_displayed(self):
        pass