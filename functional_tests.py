from selenium import webdriver
from django.test import LiveServerTestCase


class TestCreateNewClass(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()