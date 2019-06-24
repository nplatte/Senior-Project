from django.test import TestCase
from .models import Course, MyHTMLParser
from os import listdir


class TestCourseModel(TestCase):
    
    def test_uploads_to_class_htmls(self):
        test_class = Course()
        pre_up = len(listdir('C:\Users\nplat\OneDrive\Desktop\Senior Project\Class\class_htmls'))
        post_up = len(listdir('C:\Users\nplat\OneDrive\Desktop\Senior Project\Class\class_htmls'))


class TestMyHTMLParser(TestCase):

    def test_parser_pulls_course_title(self):
        HtmlPars = MyHTMLParser()
        HtmlPars.feed(
            '<th colspan="12"><span class="left"><span>Class List 2019 May Term | Undergraduate | CS 260 01 | Introduction to Computer Graphics (17 students)</span></span><span class="right"></span></th>'
            )
        self.assertEqual(HtmlPars.course_title, 'CS 260 01')

    def test_feed_full_file(self):
        pass
        