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

    def test_Course_uses_database(self):
        course = Course.objects.all().first()
        self.assertEqual(course.title, 'Introduction to Computer Graphics')
        self.assertEqual(course.term, '2019 May Term')
        self.assertEqual(course.code, 'CS 260 01')

    def test_Course_correctly_pulls_different_course_info(self):
        new_class = Course()
        new_class.create('C:\\Users\\nplat\\OneDrive\\Desktop\\Senior Project\\Class\\test_class_htmls\\ClassList.xls')
        self.assertEqual(new_class.code, 'CS 220 01')
        self.assertEqual(new_class.term, '2019 Winter Term')
        self.assertEqual(new_class.title, 'Obj-Orient Prog & Intro Data Struct')


class TestMyHTMLParser(TestCase):

    def setUp(self):
        self.parser = MyHTMLParser()

    def test_feed_full_file(self):
        self.parser.feed_file('C:\\Users\\nplat\\OneDrive\\Desktop\\Senior Project\\Class\\test_class_htmls\\original_file.xls')
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
        self.parser.feed_file('C:\\Users\\nplat\\OneDrive\\Desktop\\Senior Project\\Class\\test_class_htmls\\original_file.xls')
        self.parser.sort_data_list('\t\t\t', '\t\t')
        self.assertIn(['\t\t\t', 'Class List 2019 May Term | Undergraduate | CS 260 01 | Introduction to Computer Graphics (17 students)'], self.parser.data_list)

    def test_parses_other_courses(self):
        self.parser.feed_file('C:\\Users\\nplat\\OneDrive\\Desktop\\Senior Project\\Class\\test_class_htmls\\ClassList.xls')
        self.parser.sort_data_list()
        self.assertEqual(self.parser.data_list[0][1], 'Class List 2019 Winter Term | Undergraduate | CS 220 01 | Obj-Orient Prog & Intro Data Struct (23 students)')

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

    
