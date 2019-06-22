from django.test import TestCase
from .models import Course

class TestCourseModel(TestCase):

    def test_Course_saves_data(self):
        test_class = Course()
        test_class.title = 'CS 120'
        test_class.professor = 'Zelle'
        test_class.save()

        attributes = Course.objects.filter(title='CS 120')
        print(attributes)
        self.assertEqual(title, 'CS 120')
        self.assertEqual(prof, 'Zelle')