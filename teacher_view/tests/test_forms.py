from django.test import TestCase
from teacher_view.models import MyHTMLParser
from teacher_view.forms import CourseModelForm
from teacher_view.models import Course
from os import getcwd
from django.core.files.uploadedfile import SimpleUploadedFile

class TestCourseModelForm(TestCase):

    def setUp(self):
        self.test_form = CourseModelForm
        self.base_path = getcwd()

    def test_successful_form_saves_to_database(self):
        courses = Course.objects.all()
        self.assertEqual(len(courses), 0)
        f = open(f'{self.base_path}\\Class\\test_class_htmls\\CS_260.xls', 'r')
        ofile = SimpleUploadedFile(f'{self.base_path}\\Class\\test_class_htmls\\CS_260.xls', bytes(f.read(), 'utf-8'))
        form = self.test_form({}, {'Class_File': ofile})
        self.assertEqual(len(form.errors), 0) 
        courses = Course.objects.all()
        self.assertEqual(len(courses), 1)

    def test_form_file_type_is_xls(self):
        courses = Course.objects.all()
        self.assertEqual(len(courses), 0)
        f = open(f'{self.base_path}\\Class\\test_class_htmls\\CS_260.txt', 'r')
        ofile = SimpleUploadedFile(f'{self.base_path}\\Class\\test_class_htmls\\CS_260.txt', bytes(f.read(), 'utf-8'))
        form = self.test_form({}, {'Class_File': ofile})
        self.assertEqual(len(form.errors), 1)
        self.assertEqual('file is not .xls file', form.errors['Class_File'][0]) 


class TestMyHTMLParser(TestCase):

    def setUp(self):
        self.parser = MyHTMLParser()
        self.base_path = getcwd()

    def test_feed_full_file(self):
        self.parser.feed_file(f'{self.base_path}\\Class\\test_class_htmls\\CS_260.xls')
        first_data = '\t\t'
        last_data = '\t\t'
        self.assertEqual(first_data, self.parser.data_list[0])
        self.assertEqual(last_data, self.parser.data_list[-1])

    def test_sort_list_based_on_start_stop(self):
        self.parser.data_list = ['a', 'start', 'b', 'o', 'stop', 'a', 'stop', 'start', 'b', 'stop', 'a']
        slist_key = [['b', 'o'], ['b']]
        self.parser.sort_data_list('start', 'stop')
        self.assertEqual(slist_key, self.parser.data_list)

    def test_list_has_course_info(self):
        self.parser.feed_file(f'{self.base_path}\\Class\\test_class_htmls\\CS_260.xls')
        self.parser.sort_data_list('\t\t\t', '\t\t')
        self.assertIn(['\t\t\t', 'Class List 2019 May Term | Undergraduate | CS 260 01 | Introduction to Computer Graphics (17 students)'], self.parser.data_list)

    def test_parses_other_courses(self):
        self.parser.feed_file(f'{self.base_path}\\Class\\test_class_htmls\\CS_220.xls')
        self.parser.sort_data_list()
        self.assertEqual(self.parser.data_list[0][1], 'Class List 2019 Winter Term | Undergraduate | CS 220 01 | Obj-Orient Prog & Intro Data Struct (23 students)')
