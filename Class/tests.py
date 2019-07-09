from django.test import TestCase
from .models import Course, MyHTMLParser, Student, Assignment
from os import listdir
from django.contrib.auth.models import User


class TestAssignmentModel(TestCase):

    def setUp(self):
        self.test_assignment = Assignment()
        self.test_assignment.save()

    def tearDown(self):
        pass

    def test_assignment_has_course(self):
        cs_260 = Course()
        cs_260.create('C:\\Users\\nplat\\OneDrive\\Desktop\\Senior Project\\Class\\test_class_htmls\\CS_260.xls')
        self.test_assignment.course = cs_260
        self.assertEqual(self.test_assignment.course, Course.objects.get(code='CS 260 01'))

    def test_assignment_has_title_and_body(self):
        self.test_assignment.title = 'Make List'
        self.test_assignment.description = 'List description'
        self.assertEqual(self.test_assignment.title, 'Make List')
        self.assertEqual(self.test_assignment.description, 'List description')


class TestCourseModel(TestCase):
    
    def setUp(self):
        self.test_class = Course()
        self.test_class.create('C:\\Users\\nplat\\OneDrive\\Desktop\\Senior Project\\Class\\test_class_htmls\\CS_260.xls')
    
    def test_course_has_info(self):
        self.assertEqual(self.test_class.code, 'CS 260 01')
        self.assertEqual(self.test_class.term, '2019 May Term')
        self.assertEqual(self.test_class.title, 'Introduction to Computer Graphics')

    def test_Course_uses_database(self):
        course = Course.objects.all().first()
        self.assertEqual(course.title, 'Introduction to Computer Graphics')
        self.assertEqual(course.term, '2019 May Term')
        self.assertEqual(course.code, 'CS 260 01')

    def test_Course_correctly_pulls_different_course_info(self):
        new_class = Course()
        new_class.create('C:\\Users\\nplat\\OneDrive\\Desktop\\Senior Project\\Class\\test_class_htmls\\CS_220.xls')
        self.assertEqual(new_class.code, 'CS 220 01')
        self.assertEqual(new_class.term, '2019 Winter Term')
        self.assertEqual(new_class.title, 'Obj-Orient Prog & Intro Data Struct')

    def test_Course_does_not_duplicate_students(self):
        self.test_class.create('C:\\Users\\nplat\\OneDrive\\Desktop\\Senior Project\\Class\\test_class_htmls\\CS_260_extra_student.xls')
        students = self.test_class.students.filter(number='868019')
        self.assertEqual(students.count(), 1)

    def test_Course_only_has_students_in_xls_file_listed(self):
        cs_220 = Course()
        cs_220.create('C:\\Users\\nplat\\OneDrive\\Desktop\\Senior Project\\Class\\test_class_htmls\\CS_220.xls')
        
    def test_Course_has_instructor(self):
        test_teacher = User().save()
        self.test_class.course_instructor = test_teacher
        self.assertEqual(self.test_class.course_instructor, User.objects.all().first())
        
class TestMyHTMLParser(TestCase):

    def setUp(self):
        self.parser = MyHTMLParser()

    def test_feed_full_file(self):
        self.parser.feed_file('C:\\Users\\nplat\\OneDrive\\Desktop\\Senior Project\\Class\\test_class_htmls\\CS_260.xls')
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
        self.parser.feed_file('C:\\Users\\nplat\\OneDrive\\Desktop\\Senior Project\\Class\\test_class_htmls\\CS_260.xls')
        self.parser.sort_data_list('\t\t\t', '\t\t')
        self.assertIn(['\t\t\t', 'Class List 2019 May Term | Undergraduate | CS 260 01 | Introduction to Computer Graphics (17 students)'], self.parser.data_list)

    def test_parses_other_courses(self):
        self.parser.feed_file('C:\\Users\\nplat\\OneDrive\\Desktop\\Senior Project\\Class\\test_class_htmls\\CS_220.xls')
        self.parser.sort_data_list()
        self.assertEqual(self.parser.data_list[0][1], 'Class List 2019 Winter Term | Undergraduate | CS 220 01 | Obj-Orient Prog & Intro Data Struct (23 students)')

class TestStudentModel(TestCase):

    def setUp(self):
        self.test_class = Course()
        self.test_class.create('C:\\Users\\nplat\\OneDrive\\Desktop\\Senior Project\\Class\\test_class_htmls\\CS_260.xls')

    def test_student_has_name(self):
        test_student = Student.objects.filter(name = 'Platte, Nathan Wayne').first()
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