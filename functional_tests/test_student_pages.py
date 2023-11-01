from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from time import sleep
from os import remove
from teacher_view.models import Course


class TestTeacherAssignmentPost(LiveServerTestCase):

    def setUp(self):

        self.browser = webdriver.Firefox()
        self.browser.get(f'{self.live_server_url}/admin/')

    def tearDown(self):
        self.browser.quit()

    def teacher_login(self, username, password):
        username_input = self.browser.find_element_by_name('username')
        username_input.send_keys(username)
        password_input = self.browser.find_element_by_name('password')
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

    def test_teacher_post_assignment(self):
        # A professor goes to the django admin site
        # They proceed to login using their credentials
        self.teacher_login('test_staff', 'Sparta12456')

        # They click the courses button which takes them to their courses list
        # They see only the courses that are assigned to them with the courses in term order
        self.browser.get(f'{self.live_server_url}/admin/Class/course/')
        # they click on the most recent course
        # this takes them to the course home page
        # This lists all the students in the course, recent activity, open assignments and closed assignments
        # under open assignments there is an add new assignment at the top
        # the teacher clicks that button
                