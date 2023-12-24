from django.test import TestCase
from django.contrib.auth.models import User, Group
from teacher_view.models import Course

class ViewTest(TestCase):

    def setUp(self) -> None:
        self.test_user = self._add_staff_user()
        self.client.force_login(self.test_user)
        self.c = self._make_course(self.test_user)
        return super().setUp()

    def _add_staff_user(self):
        # inorder to login, a user must be part of the staff group
        test_user = User.objects.create_user('new', 'new@gmail.com', 'password')
        staff_group = Group.objects.create(name='staff')
        staff_group.user_set.add(test_user)
        return test_user

    def _make_course(self, user, title='test course'):
        # this makes a course with the passed user as the instructor
        term = f'2023 Fall Term'
        return Course.objects.create(title=title, course_instructor = user, term=term)