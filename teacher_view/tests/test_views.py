from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group

class TestHomePage(TestCase):

    def setUp(self):
        test_user = User.objects.create_user('new', 'new@gmail.com', 'password')
        staff_group = Group.objects.create(name='staff')
        staff_group.user_set.add(test_user)
        self.client.force_login(test_user)

    def test_home_page_uses_right_template(self):
        request = self.client.get(reverse('staff_home_page'), follow=True)
        self.assertTemplateUsed(request, 'teacher_view/home.html')


class TestProfilePage(TestCase):

    def setUp(self):
        test_user = User.objects.create_user('new', 'new@gmail.com', 'password')
        staff_group = Group.objects.create(name='staff')
        staff_group.user_set.add(test_user)
        self.client.force_login(test_user)

    def test_profile_page_uses_right_template(self):
        request = self.client.get(reverse('staff_profile_page'), follow=True)
        self.assertTemplateUsed(request, 'teacher_view/profile.html')


class TestAddCoursePage(TestCase):

    def setUp(self):
        pass