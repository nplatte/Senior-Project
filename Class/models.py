from django.db import models
from html.parser import HTMLParser



class Course(models.Model):
    
    Class_File = models.FileField(upload_to='class_htmls')


class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        course_info = data.split(' | ')
        self.course_title = course_info[2]