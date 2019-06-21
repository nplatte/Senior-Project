from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from time import sleep


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
        self.admin_login('admin', 'E!byz..D)4P!M4')
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
        self.admin_login('admin', 'E!byz..D)4P!M4')
        sleep(1)
        self.assertNotIn('OperationalError ', self.browser.title)

        # The admin user selects the create class option on the page
        # The admin is taken to a page where they choose to upload a file in html format
        # After puting in more information, they are taken to their new class page displaying student information like numbers, names, and emails
        # This page has the course title, the term, and prefessor name on the top