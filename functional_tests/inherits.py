from selenium import webdriver
from django.test import LiveServerTestCase
from django.contrib.auth.models import User, Group

class BasicSeleniumTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.test_user = User.objects.create_user('new', 'new@gmail.com', 'password')
        staff_group = Group.objects.create(name='staff')
        staff_group.user_set.add(self.test_user)
        self.browser = webdriver.Firefox()
        return super().setUp()