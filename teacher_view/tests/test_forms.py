from django.test import TestCase
#from teacher_view.models import MyHTMLParser
from teacher_view.forms import CourseModelFileForm, MyHTMLParser
from teacher_view.models import Course
from os import getcwd
from django.core.files.uploadedfile import InMemoryUploadedFile

class TestCourseModelFileForm(TestCase):

    def setUp(self):
        self.base_path = f'{getcwd()}\\teacher_view\\test_class_htmls'
        file = open(f'{self.base_path}\\CS_220_May.xls')
        imf = InMemoryUploadedFile(
            file=file,
            field_name='source_file',
            name='CS_220_May.xls',
            content_type='application/vnd.ms-excel',
            size=14054,
            charset=None,
            content_type_extra={}
        )
        self.test_data = ({}, {'source_file': imf})
        

    def test_good_file_is_valid(self): 
        form = CourseModelFileForm(*self.test_data)
        self.assertTrue(form.is_valid())
        

    def test_successful_form_saves_to_database(self):
        courses = Course.objects.all()
        self.assertEqual(len(courses), 0)
        form = CourseModelFileForm(*self.test_data)
        self.assertEqual(len(form.errors), 0)
        form.save() 
        courses = Course.objects.all()
        self.assertEqual(len(courses), 1)  

    def test_form_file_type_is_xls(self):
        file = open(f'{self.base_path}\\CS_260.txt')
        imf = InMemoryUploadedFile(
            file=file,
            field_name='source_file',
            name='CS_260.txt',
            content_type='text/plain',
            size=14054,
            charset=None,
            content_type_extra={}
        )
        form = CourseModelFileForm({}, {'source_file': imf})
        self.assertEqual(len(form.errors), 1)
        self.assertEqual('source file is not .xls file', form.errors['source_file'][0])


class TestMyHTMLParser(TestCase):

    def setUp(self):
        self.parser = MyHTMLParser()
        self.base_path = f'{getcwd()}\\teacher_view\\test_class_htmls'

    def test_feed_full_file(self):
        
        self.parser.feed_file(f'{self.base_path}\\CS_260.xls')
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
        self.parser.feed_file(f'{self.base_path}\\CS_260.xls')
        self.parser.sort_data_list('\t\t\t', '\t\t')
        self.assertIn(['\t\t\t', 'Class List 2019 May Term | Undergraduate | CS 260 01 | Introduction to Computer Graphics (17 students)'], self.parser.data_list)

    def test_parses_other_courses(self):
        self.parser.feed_file(f'{self.base_path}\\CS_220.xls')
        self.parser.sort_data_list()
        self.assertEqual(self.parser.data_list[0][1], 'Class List 2019 Winter Term | Undergraduate | CS 220 01 | Obj-Orient Prog & Intro Data Struct (23 students)')
