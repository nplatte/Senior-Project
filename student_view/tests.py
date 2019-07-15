from django.test import TestCase
from django.urls import resolve
from django.http import HttpResponse

from .views import home_page


class HomePageTest(TestCase):

    def test_root_url(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpResponse()
        response = home_page(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Student Profile</title>')
        self.assertTrue(html.endswith('<html>'))

    def test_fetches_queryset_of_assignments(self):
        

