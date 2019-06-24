from django.test import TestCase
from .models import Course, MyHTMLParser
from os import listdir


class TestCourseModel(TestCase):
    
    pass

class TestMyHTMLParser(TestCase):

    def test_feed_full_file(self):
        HtmlPars = MyHTMLParser()
        HtmlPars.feed_file('C:\\Users\\nplat\\OneDrive\\Desktop\\Senior Project\\Class\\test_class_htmls\\original_file.xls')
        first_data = '\t\t'
        last_data = '\t\t'
        self.assertEqual(first_data, HtmlPars.data_list[0])
        self.assertEqual(last_data, HtmlPars.data_list[-1])

    def test_sort_list_based_on_start_stop(self):
        HtmlPars = MyHTMLParser()
        HtmlPars.data_list = ['a', 'start', 'b', 'o', 'stop', 'a', 'stop', 'start', 'b', 'stop', 'a']
        slist_key = ['b', 'o', 'b']
        sorted_list = HtmlPars.sort_data_list('start', 'stop')
        self.assertEqual(slist_key, sorted_list)

    def test_list_has_course_info(self):
        HtmlPars = MyHTMLParser()
        HtmlPars.feed_file('C:\\Users\\nplat\\OneDrive\\Desktop\\Senior Project\\Class\\test_class_htmls\\original_file.xls')
        