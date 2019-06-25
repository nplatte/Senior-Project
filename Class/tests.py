from django.test import TestCase
from .models import Course, MyHTMLParser, Student
from os import listdir


class TestCourseModel(TestCase):
    
    def test_course_has_info(self):
        test_class = Course()
        test_class.create('C:\\Users\\nplat\\OneDrive\\Desktop\\Senior Project\\Class\\test_class_htmls\\original_file.xls')
        self.assertEqual(test_class.code, 'CS 260 01')
        self.assertEqual(test_class.term, '2019 May Term')
        self.assertEqual(test_class.title, 'Introduction to Computer Graphics')


class TestMyHTMLParser(TestCase):

    def test_feed_full_file(self):
        HtmlPars = MyHTMLParser()
        HtmlPars.feed_file('C:\\Users\\nplat\\OneDrive\\Desktop\\Senior Project\\Class\\test_class_htmls\\original_file.xls')
        first_data = '\t\t'
        last_data = '\t\t'
        self.assertEqual(first_data, HtmlPars.data_list[0])
        self.assertEqual(last_data, HtmlPars.data_list[-1])

    def test_sort_list_based_on_start_stop(self):
        HtmlPars = MyHTMLParser()
        HtmlPars.data_list = ['a', 'start', 'b', 'o', 'stop', 'a', 'stop', 'start', 'b', 'stop', 'a']
        slist_key = [['b', 'o'], ['b']]
        HtmlPars.sort_data_list('start', 'stop')
        self.assertEqual(slist_key, HtmlPars.data_list)

    def test_list_has_course_info(self):
        HtmlPars = MyHTMLParser()
        HtmlPars.feed_file('C:\\Users\\nplat\\OneDrive\\Desktop\\Senior Project\\Class\\test_class_htmls\\original_file.xls')
        HtmlPars.sort_data_list('\t\t\t', '\t\t')
        self.assertIn(['\t\t\t', 'Class List 2019 May Term | Undergraduate | CS 260 01 | Introduction to Computer Graphics (17 students)'], HtmlPars.data_list)


class TestStudentModel(TestCase):

    def setUp(self):
        test_class = Course()
        test_class.create('C:\\Users\\nplat\\OneDrive\\Desktop\\Senior Project\\Class\\test_class_htmls\\original_file.xls')

    def test_student_has_name(self):
        test_student = Student()