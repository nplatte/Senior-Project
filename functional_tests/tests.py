from selenium import webdriver
from unittest import TestCase

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert 'Django' in browser.title

class TestCreateNewClass(TestCase):

    pass