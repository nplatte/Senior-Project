from django.test import TestCase
from django.utils.timezone import datetime
from teacher_view.forms import CourseModelFileForm, MyHTMLParser, EditCourseForm, AssignmentForm
from teacher_view.models import Course
from os import getcwd, remove, path
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User
import zoneinfo

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

    def tearDown(self) -> None:
        upload_file = f'{getcwd()}\\class_htmls\\CS_220_May.xls'
        if path.exists(upload_file):
            remove(upload_file)
        return super().tearDown()
        
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

    def test_saving_form_assigns_course_info(self):
        form = CourseModelFileForm(*self.test_data)
        self.assertEqual(len(form.errors), 0)
        new_course = form.save()

        self.assertEqual(new_course.title, 'Obj-Orient Prog & Intro Data Struct')
        self.assertEqual(new_course.code, 'CS 220 01')
        self.assertEqual(new_course.term, 'May Term')


class TestEditCourseForm(TestCase):

    def setUp(self):
        instr = User.objects.create_user('test', 'test@test.com', 'p@ssword')
        self.base_path = f'{getcwd()}\\teacher_view\\test_class_htmls'
        file = open(f'{self.base_path}\\CS_260.xls')
        imf = InMemoryUploadedFile(
            file=file,
            field_name='source_file',
            name='CS_260.xls',
            content_type='application/vnd.ms-excel',
            size=14054,
            charset=None,
            content_type_extra={}
        )
        self.c = Course.objects.create(
            source_file=imf,
            code='CS 260 01',
            title='Introduction to Comp',
            term='2024 May Term',
            course_instructor=instr
        )

    def tearDown(self) -> None:
        upload_file = f'{getcwd()}\\class_htmls\\CS_260.xls'
        if path.exists(upload_file):
            remove(upload_file)
        return super().tearDown()

    def test_good_form_success(self):
        data = {
            'title': 'Intro to Graphics',
            'code': 'CS 250 01',
            'term': '2025 May Term'
        }
        form = EditCourseForm(data=data, instance=self.c)
        self.assertTrue(form.is_valid())
        form.save()
        new_title = self.c.title
        new_code = self.c.code
        new_term = self.c.term
        self.assertEqual(new_title, data['title'])
        self.assertEqual(new_code, data['code'])
        self.assertEqual(new_term, data['term'])

    def test_form_attributes(self):
        form = EditCourseForm()
        f_as_p = form.as_p()
        self.assertIn('id="edit-course-title"', f_as_p)
        self.assertIn('id="edit-course-code"', f_as_p)
        self.assertIn('id="edit-course-term"', f_as_p)
        

class TestAssignmentForm(TestCase):

    def setUp(self) -> None:
        self.data = {
            'title': 'Test Assignment',
            'description': 'this is bout the assignment',
            'due_date': datetime(2024, 12, 30, 12, 12, 1, tzinfo=zoneinfo.ZoneInfo(key='America/Panama')),
            'display_date': datetime(2024, 12, 23, 12, 12, 1, tzinfo=zoneinfo.ZoneInfo(key='America/Panama'))
        }
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_good_form_is_valid(self):
        form = AssignmentForm(self.data)
        self.assertTrue(form.is_valid())

    def test_form_has_correct_ids(self):
        form = AssignmentForm(self.data)
        self.assertIn('id="a-title-input"', form.as_p())
        self.assertIn('id="a-due-date-input"', form.as_p())
        self.assertIn('id="a-description-input"', form.as_p())
        self.assertIn('id="a-display-date-input"', form.as_p())

    def test_form_makes_assignment(self):
        form = AssignmentForm(self.data)
        a = form.save()
        self.assertEqual(a.title, self.data['title'])
        self.assertEqual(a.description, self.data['description'])
        self.assertEqual(a.due_date, self.data['due_date'])
        self.assertEqual(a.display_date, self.data['display_date'])


class TestMyHTMLParser(TestCase):

    def setUp(self):
        self.parser = MyHTMLParser()
        self.base_path = f'{getcwd()}\\teacher_view\\test_class_htmls'

    def tearDown(self) -> None:
        upload_file = f'{getcwd()}\\class_htmls\\CS_260.xls'
        if path.exists(upload_file):
            remove(upload_file)
        return super().tearDown()

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
