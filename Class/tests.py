from django.test import TestCase
from .models import Course, MyHTMLParser, Student
from os import listdir


class TestCourseModel(TestCase):
    
    def setUp(self):
        self.test_class = Course()
        self.test_class.create('C:\\Users\\nplat\\OneDrive\\Desktop\\Senior Project\\Class\\test_class_htmls\\original_file.xls')
    
    def test_course_has_info(self):
        self.assertEqual(self.test_class.code, 'CS 260 01')
        self.assertEqual(self.test_class.term, '2019 May Term')
        self.assertEqual(self.test_class.title, 'Introduction to Computer Graphics')

    def test_add_students_to_list(self):
        self.test_class.add_students()
        self.assertEqual(17, len(self.test_class.Students))


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
        self.test_class = Course()
        self.test_class.create('C:\\Users\\nplat\\OneDrive\\Desktop\\Senior Project\\Class\\test_class_htmls\\original_file.xls')
        self.test_class.add_students()

    def test_student_has_name(self):
        test_student = self.test_class.Students[9]
        self.assertEqual(test_student.name, 'Platte, Nathan Wayne')

    def test_student_saves_to_database(self):
        test_student = Student()
        test_student.add_info(['\t\t\t', 'N', '868019', 'Platte, Nathan Wayne', 'H - History', '\xa0', 'nathan.platte@wartburg.edu', '\xa0', 'Computer Science', 'Fourth Year'])
        
        self.assertEqual(len(Student.objects.all()), 18)
        student = Student.objects.filter(email='nathan.platte@wartburg.edu').first()
        self.assertEqual(student.name, 'Platte, Nathan Wayne')

    def test_student_has_all_info(self):
        student = Student.objects.filter(name='Hookham, Trey Charles').first()
        self.assertEqual(student.email, 'trey.hookham@wartburg.edu')
        self.assertEqual(student.number, 1129224)
        self.assertEqual(student.year, 'Fourth Year')