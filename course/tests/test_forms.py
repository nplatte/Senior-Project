from django.test import TestCase
from course.forms import CourseModelFileForm, MyHTMLParser, EditCourseForm
from course.models import Course
from os import getcwd, remove, path
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User

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
            term='May Term',
            year='23-24',
            instructor=instr
        )
        self.data = {
            'title': 'Intro to Graphics',
            'code': 'CS 250 01',
            'term': 'May Term',
            'year': '24-25',
            'instructor': instr
        }

    def tearDown(self) -> None:
        upload_file = f'{getcwd()}\\class_htmls\\CS_260.xls'
        if path.exists(upload_file):
            remove(upload_file)
        return super().tearDown()

    def test_good_form_success(self):
        form = EditCourseForm(data=self.data, instance=self.c)
        self.assertTrue(form.is_valid())
        form.save()
        new_title = self.c.title
        new_code = self.c.code
        new_term = self.c.term
        self.assertEqual(new_title, self.data['title'])
        self.assertEqual(new_code, self.data['code'])
        self.assertEqual(new_term, self.data['term'])
        self.assertEqual(self.c.year, self.data['year'])

    def test_form_attributes(self):
        form = EditCourseForm()
        f_as_p = form.as_p()
        self.assertIn('id="edit-course-title"', f_as_p)
        self.assertIn('id="edit-course-code"', f_as_p)
        self.assertIn('id="edit-course-term"', f_as_p)

    def _field_throws_error_when_absent(self, field_name):
        del self.data[field_name]
        form = EditCourseForm(self.data, instance=self.c)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors[field_name][0], 'This field is required.')

    def test_no_title_throws_error(self):
        self._field_throws_error_when_absent('title')
        self._field_throws_error_when_absent('code')
        self._field_throws_error_when_absent('term')
        self._field_throws_error_when_absent('year')

    def test_accepted_terms(self):
        terms = ['Summer Term', 'Fall Term',
            'May Term', 'Winter Term']
        for term in terms:
            self.data['term'] = term
            form = EditCourseForm(self.data, instance=self.c)
            self.assertTrue(form.is_valid())

    def test_bad_term(self):
        bad_term = 'Polka Term'
        self.data['term'] = bad_term
        form = EditCourseForm(self.data, instance=self.c)
        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors['term']))
        self.assertEqual(form.errors['term'][0], f"Term {bad_term} not in ['Summer Term', 'Fall Term', 'May Term', 'Winter Term']")


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
