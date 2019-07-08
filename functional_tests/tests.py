from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from time import sleep
from os import remove
from Class.models import Course


class TestTeacherAssignmentPost(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_teacher_login(self):
        pass


class TestCreateNewClass(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def admin_login(self, username, password):
        username_input = self.browser.find_element_by_name('username')
        username_input.send_keys(username)
        password_input = self.browser.find_element_by_name('password')
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

    def test_admin_can_make_other_admins(self):
        # The admin opens their browser
        self.browser.get('http://localhost:8000')

        # An admin goes to the Django admin page
        self.browser.get('http://localhost:8000/admin/')
        self.assertIn('admin', self.browser.title)

        # The admin logs into the admin page
        self.admin_login('nathan.platte', 'Sparta12456')
        sleep(1)
        self.assertNotIn('OperationalError ', self.browser.title)

        # The admin clicks the add user
        # The admin then has a list of other users to make admins
        # The admin then puts in the first name
        # The first email
        # and the password for the new admin

    def test_create_new_class(self):
        # An admin user wants to create a new class page using the html file with student information
        # They open their browser
        self.browser.get('http://localhost:8000')

        # They go to the django admin site
        self.browser.get('http://localhost:8000/admin/')
        self.assertIn('admin', self.browser.title)

        # They log in using their credentials
        self.admin_login('nathan.platte', 'Sparta12456')
        sleep(1)
        self.assertNotIn('OperationalError ', self.browser.title)

        # The admin user selects the create class option on the page
        self.browser.get('http://localhost:8000/admin/Class/course/add/')


        # The admin is taken to a page where they choose to upload an .xls file and no other information        
        # the admin chooses the file and uploads it and presses the save button
        file_upload = self.browser.find_element_by_name('Class_File')
        file_upload.send_keys('C:\\Users\\nplat\\OneDrive\\Desktop\\Senior Project\\Class\\test_class_htmls\\cs_220.xls')
        save_course = self.browser.find_element_by_name('_save')
        save_course.click()

        
        saved_course = Course.objects.all().first()
        self.assertEqual(saved_course.title, 'Introduction to Computer Graphics')
        self.assertEqual(saved_course.term, '2019 May Term')
        self.assertEqual(saved_course.code, 'CS 260 01')
        
        remove('C:\\Users\\nplat\\OneDrive\\Desktop\\Senior Project\\class_htmls\\cs_220.xls')

        # They are shown a display page, previewing the information
        self.assertEqual(self.browser.current_url, 'http://localhost:8000/admin/Class/course/preview/')
        # This page has the course title, the term, and prefessor name on the top and the students displayed below



        