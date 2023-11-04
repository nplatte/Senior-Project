from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group


def _add_staff_user():
    test_user = User.objects.create_user('new', 'new@gmail.com', 'password')
    staff_group = Group.objects.create(name='staff')
    staff_group.user_set.add(test_user)
    return test_user


class TestHomePage(TestCase):

    def setUp(self):
        test_user = _add_staff_user()
        self.client.force_login(test_user)

    def test_home_page_uses_right_template(self):
        request = self.client.get(reverse('staff_home_page'), follow=True)
        self.assertTemplateUsed(request, 'teacher_view/home.html')


class TestProfilePage(TestCase):

    def setUp(self):
        test_user = _add_staff_user()
        self.client.force_login(test_user)

    def test_profile_page_uses_right_template(self):
        request = self.client.get(reverse('staff_profile_page'), follow=True)
        self.assertTemplateUsed(request, 'teacher_view/profile.html')


class TestAddCoursePage(TestCase):

    def setUp(self):
        test_user = _add_staff_user()
        self.client.force_login(test_user)

    def test_page_uses_right_template(self):
        request = self.client.get(reverse('staff_add_course_page'), follow=True)
        self.assertTemplateUsed(request, 'teacher_view/create_class.html')

    def test_page_passes_current_courses_to_navbar(self):
        pass 