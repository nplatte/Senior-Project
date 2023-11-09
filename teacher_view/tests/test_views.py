from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from teacher_view.models import Course
from datetime import date
from teacher_view.forms import CourseModelForm
from os import getcwd


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
        self.assertIsInstance(form, CourseModelForm)

    def test_file_upload_form_redirects_to_new_course_page(self):
        pth = f'{getcwd()}\\class_htmls\\CS_220_May.xls'
        ofile = open(pth)
        data = {
            'Class_File': ofile
        }
        request = self.client.post(reverse('staff_add_course_page'), follow=True, data=data)
        self.assertRedirects(request, 'teacher_view/course.html')

    def test_file_upload_creates_new_course(self):
        courses = len(Course.objects.all())
        self.assertEqual(0, courses)
        pth = f'{getcwd()}\\class_htmls\\CS_220_May.xls'
        ofile = open(pth)
        data = {
            'Class_File': ofile
        }
        request = self.client.post(reverse('staff_add_course_page'), follow=True, data=data)
        courses = len(Course.objects.all())
        self.assertEqual(1, courses)
