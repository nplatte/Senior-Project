from django.test import TestCase
from teacher_view.models import Assignment
from os import getcwd



class TestAssignmentModel(TestCase):

    def setUp(self):
        self.test_assignment = Assignment()
        self.test_assignment.save()
        self.base_path = f'{getcwd()}\\teacher_view\\test_class_htmls'

    def tearDown(self):
        pass

    def test_assignment_has_title_and_body(self):
        self.test_assignment.title = 'Make List'
        self.test_assignment.description = 'List description'
        self.assertEqual(self.test_assignment.title, 'Make List')
        self.assertEqual(self.test_assignment.description, 'List description')
