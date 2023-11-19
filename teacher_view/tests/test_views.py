from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from teacher_view.models import Course
from datetime import date
from teacher_view.forms import CourseModelFileForm, EditCourseForm
from django.core.files.uploadedfile import InMemoryUploadedFile
from os import getcwd, remove, path


def _add_staff_user():
    test_user = User.objects.create_user('new', 'new@gmail.com', 'password')
    staff_group = Group.objects.create(name='staff')
    staff_group.user_set.add(test_user)
    return test_user

def _make_class(user):
    term = f'2023 Fall Term'
    return Course.objects.create(title='test course', course_instructor = user, term=term)


class TestHomePage(TestCase):

    def setUp(self):
        self.test_user = _add_staff_user()
        self.client.force_login(self.test_user)

    def test_home_page_uses_right_template(self):
        request = self.client.get(reverse('staff_home_page'), follow=True)
        self.assertTemplateUsed(request, 'teacher_view/home.html')

    def test_home_page_passes_current_classes_for_navbar(self):
        new_course = _make_class(self.test_user)
        request = self.client.get(reverse('staff_home_page'))
        course_list = request.context['current_courses']
        self.assertIn(new_course, course_list)


class TestProfilePage(TestCase):

    def setUp(self):
        self.test_user = _add_staff_user()
        self.client.force_login(self.test_user)

    def test_profile_page_uses_right_template(self):
        request = self.client.get(reverse('staff_profile_page'), follow=True)
        self.assertTemplateUsed(request, 'teacher_view/profile.html')

    def test_profile_page_passes_current_courses_to_navbar(self):
        new_course = _make_class(self.test_user)
        request = self.client.get(reverse('staff_profile_page'))
        course_list = request.context['current_courses']
        self.assertIn(new_course, course_list)


class TestAddCoursePage(TestCase):

    def setUp(self):
        self.test_user = _add_staff_user()
        self.client.force_login(self.test_user)

    def test_add_course_login_required(self):
        self.client.logout()
        request = self.client.get(reverse('staff_add_course_page'), follow=True)
        self.assertTemplateUsed(request, 'login/login.html')

    def test_page_uses_right_template(self):
        request = self.client.get(reverse('staff_add_course_page'), follow=True)
        self.assertTemplateUsed(request, 'teacher_view/create_class.html')

    def test_add_courses_passes_current_courses_to_navbar(self):
        new_course = _make_class(self.test_user)
        request = self.client.get(reverse('staff_add_course_page'))
        courses = request.context['current_courses']
        self.assertIn(new_course, courses)

    def test_file_upload_form_is_passed_to_page(self):
        request = self.client.get(reverse('staff_add_course_page'))
        form = request.context['file_form']
        self.assertIsInstance(form, CourseModelFileForm)

    def test_file_upload_form_redirects_to_new_course_page(self):
        pth = f'{getcwd()}\\class_htmls\\CS_220_May.xls'
        ofile = open(pth)
        data = {
            'source_file': ofile
        }
        request = self.client.post(reverse('staff_add_course_page'), follow=True, data=data)
        self.assertRedirects(request, '/teacher/course/1/')

    def test_file_upload_creates_new_course(self):
        courses = len(Course.objects.all())
        self.assertEqual(0, courses)
        pth = f'{getcwd()}\\class_htmls\\CS_220_May.xls'
        ofile = open(pth)
        data = {
            'source_file': ofile
        }
        request = self.client.post(reverse('staff_add_course_page'), follow=True, data=data)
        courses = len(Course.objects.all())
        self.assertEqual(1, courses)


class TestEditCoursePage(TestCase):

    def setUp(self):
        self.test_user = _add_staff_user()
        self.client.force_login(self.test_user)
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
        c = Course.objects.create(
            source_file=imf,
            code='CS 260 01',
            title='Introduction to Comp',
            term='2024 May Term',
            course_instructor=self.test_user
        )
    
    def tearDown(self) -> None:
        upload_dir = f'{getcwd()}\\class_htmls'
        if path.exists(f'{upload_dir}\\CS_260.xls'):
            remove(f'{upload_dir}\\CS_260.xls')
        return super().tearDown()
    
    

    def test_returns_right_html_page(self):
        request = self.client.get(reverse('staff_edit_course_page', kwargs={'course_id': 1}))
        self.assertTemplateUsed(request, 'teacher_view/edit_course.html')

    def test_pass_current_courses_to_navbar(self):
        request = self.client.get(reverse('staff_edit_course_page', kwargs={'course_id': 1}))
        curr_courses = request.context['current_courses']
        self.assertEqual(len(curr_courses), 1)

    def test_course_uses_right_form_for_editing(self):
        request = self.client.get(reverse('staff_edit_course_page', kwargs={'course_id': 1}))
        edit_form = request.context['edit_form']
        self.assertIsInstance(edit_form, EditCourseForm)

    def test_form_has_existing_course_info(self):
        request = self.client.get(reverse('staff_edit_course_page', kwargs={'course_id': 1}))
        edit_form = request.context['edit_form']
        self.assertTrue(edit_form.is_bound)
