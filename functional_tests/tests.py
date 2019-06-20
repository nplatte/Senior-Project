from selenium import webdriver
from django.test import LiveServerTestCase


class TestCreateNewClass(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_admin_can_make_other_admins(self):
        # An admin logs into the Django admin page
        # The admin then has a list of other users to make admins
        # The admin then puts in the first name
        # The first email
        # and the password for the new admin
        pass

    def test_create_new_class(self):
        # An admin user wants to create a new class page using the html file with student information
        # They go to the django admin site
        # They log in using their credentials
        # The admin user selects the create class option on the page
        # The admin is taken to a page where they choose to upload a file in html format
        # After puting in more information, they are taken to their new class page displaying student information like numbers, names, and emails
        # This page has the course title, the term, and prefessor name on the top
        pass