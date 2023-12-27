from assignment.models import Assignment
from django.urls import reverse
from course.models import Course, Student
from course.forms import CourseModelFileForm, EditCourseForm
from django.utils.timezone import datetime
from os import getcwd, remove, path
from zoneinfo import ZoneInfo
import json
from rest_framework.test import APIRequestFactory, APITestCase
from teacher_view.tests.inherit import ViewTest


class TestViewStudentCoursesAPI(ViewTest, APITestCase):

    def setUp(self):
        super().setUp()
        self.ts = Student.objects.create(
            name='Jane Doe',
            email='jd@gmail.com',
            number=12345678,
            year=2020
        )
        self.c.students.add(self.ts)
        self.c.save()
        
        self.url = reverse('view_courses_api', kwargs={'student_id': self.ts.number})

    def test_api_requests_gets_a_course(self):
        response = self.client.get(self.url)
        expected_data = [{
            'id': self.c.pk,
            'title': self.c.title,
            'code': self.c.code,
            'term': self.c.term,
            'instructor': self.c.instructor.pk,
        }]
        self.assertJSONEqual(response.content, json.dumps(expected_data))


class TestViewCoursePage(ViewTest):

    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('view_course_page', kwargs={'course_id': self.c.pk})
        self.response = self.client.get(self.url)
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_uses_right_template(self):
        self.assertTemplateUsed(self.response, 'course/view.html')

    def test_passes_navbar_information(self):
        cc = self.response.context['current_courses']
        self.assertIn(self.c, cc)

    def passes_correct_context(self):
        c = self.response.context['course']
        self.assertEqual(c, self.c)
        assignments = self.response.context['assignments']
        self.assertEqual(len(assignments), 0)

    def test_does_not_pass_other_course_assignments(self):
        c2 = self._make_course(self.test_user, 'class 2')
        a1 = Assignment.objects.create(
            title='Make Google',
            description='make Google please',
            due_date=datetime(2024, 12, 31, 12, 12, 0, tzinfo=ZoneInfo(key='America/Panama')),
            display_date=datetime(2024, 12, 31, 12, 12, 0, tzinfo=ZoneInfo(key='America/Panama')),
            course=self.c
        )
        a2 = Assignment.objects.create(
            title='Make Google 2',
            description='make Google please 2',
            due_date=datetime(2024, 12, 31, 12, 12, 0, tzinfo=ZoneInfo(key='America/Panama')),
            display_date=datetime(2024, 12, 31, 12, 12, 0, tzinfo=ZoneInfo(key='America/Panama')),
            course=c2
        )
        response = self.client.get(reverse('view_course_page', kwargs={'course_id': self.c.pk}))
        a_list = response.context['assignments']
        self.assertIn(a1, a_list)
        self.assertNotIn(a2, a_list)


class TestAddCoursePageGET(ViewTest):

    def setUp(self):
        super().setUp()
        self.url = reverse('add_course_page')

    def tearDown(self) -> None:
        upload_file = f'{getcwd()}\\class_htmls\\CS_220_May.xls'
        if path.exists(upload_file):
            remove(upload_file)
        return super().tearDown()

    def test_add_course_login_required(self):
        self.client.logout()
        request = self.client.get(self.url, follow=True)
        self.assertTemplateUsed(request, 'login/login.html')

    def test_page_uses_right_template(self):
        request = self.client.get(self.url, follow=True)
        self.assertTemplateUsed(request, 'course/create.html')

    def test_add_courses_passes_current_courses_to_navbar(self):
        new_course = self._make_course(self.test_user)
        request = self.client.get(self.url)
        courses = request.context['current_courses']
        self.assertIn(new_course, courses)

    def test_file_upload_form_is_passed_to_page(self):
        request = self.client.get(self.url)
        form = request.context['file_form']
        self.assertIsInstance(form, CourseModelFileForm)


class TestAddCoursePagePOST(ViewTest):

    def setUp(self) -> None:
        super().setUp()
        pth = f'{getcwd()}\\teacher_view\\test_class_htmls\\CS_220_May.xls'
        ofile = open(pth)
        self.data = {
            'source_file': ofile
        }
        self.url = reverse('add_course_page')
    
    def tearDown(self) -> None:
        upload_file = f'{getcwd()}\\class_htmls\\CS_220_May.xls'
        if path.exists(upload_file):
            remove(upload_file)
        return super().tearDown()

    def test_file_upload_form_redirects_to_new_course_page(self):
        response = self.client.post(self.url, follow=True, data=self.data)
        created_course = Course.objects.filter(code='CS 220 01')[0]
        self.assertRedirects(response, created_course.get_absolute_url())

    def test_file_upload_creates_new_course(self):
        courses = len(Course.objects.all())
        self.assertEqual(1, courses)
        self.client.post(self.url, follow=True, data=self.data)
        courses = len(Course.objects.all())
        self.assertEqual(2, courses)


class TestEditCoursePageGET(ViewTest):

    def setUp(self):
        super().setUp()
        self.url = reverse('edit_course_page', kwargs={'course_id': self.c.pk})
    
    def tearDown(self) -> None:
        upload_dir = f'{getcwd()}\\class_htmls'
        if path.exists(f'{upload_dir}\\CS_260.xls'):
            remove(f'{upload_dir}\\CS_260.xls')
        return super().tearDown()  

    def test_returns_right_html_page(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'course/edit.html')

    def test_pass_current_courses_to_navbar(self):
        response = self.client.get(self.url)
        curr_courses = response.context['current_courses']
        edited_course = response.context['course']
        self.assertEqual(len(curr_courses), 1)
        self.assertEqual(self.c, edited_course)
        self.assertIsInstance(edited_course, Course)

    def test_course_uses_right_form_for_editing(self):
        response = self.client.get(self.url)
        edit_form = response.context['edit_form']
        self.assertIsInstance(edit_form, EditCourseForm)

    def test_form_has_existing_course_info(self):
        response = self.client.get(self.url)
        edit_form = response.context['edit_form'].as_p()
        self.assertIn(self.c.title, edit_form)
        self.assertIn(self.c.code, edit_form)


class TestEditCoursePagePOST(ViewTest):

    def setUp(self):
        super().setUp()
        self.data = {
            'title': 'Weird',
            'code': '1234',
            'term': 'May Term',
            'year': '23-24'
        }
        self.url = reverse('edit_course_page', kwargs={'course_id': self.c.pk})

    def test_successful_POST_redirects_to_course_page(self):
        response = self.client.post(self.url, data=self.data)
        expected_url = reverse('view_course_page', kwargs={'course_id': self.c.pk})
        self.assertRedirects(response, expected_url)

    def test_unseccessful_POST_does_not_redirect(self):
        self.data = {
            'title': 'Weird',
            'term': 'May Term',
            'year': '23-24'
        }
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('course/edit.html')

    def test_successful_form_updates_course_info(self):
        self.client.post(self.url, data=self.data)
        c = Course.objects.get(pk=self.c.pk)
        self.assertNotEqual('test course', c.title)
        self.assertEqual(self.data['title'], c.title)


class TestCoursesViewPage(ViewTest):

    def setUp(self) -> None:
        self.url = reverse('courses_page')
        super().setUp()
    
    def tearDown(self) -> None:
        upload_file = f'{getcwd()}\\class_htmls\\CS_260.xls'
        if path.exists(upload_file):
            remove(upload_file)
        return super().tearDown()
    
    def test_uses_right_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'course/courses.html')

    def test_passes_navbar_courses(self):
        request = self.client.get(self.url)
        curr_courses = request.context['current_courses']
        self.assertEqual(len(curr_courses), 1)

    def test_passes_logged_in_users_courses(self):
        non_user_course = Course.objects.create(
            code='CS 260 02',
            title='Intro to Comp',
            term= 'May Term',
            year= '23-24'
        )
        response = self.client.get(self.url)
        all_courses = response.context['all_courses']
        self.assertEqual(1, len(all_courses))
        self.assertNotIn(non_user_course, all_courses)
        self.assertIn(self.c, all_courses)
        