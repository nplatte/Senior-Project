from django.db import models
from html.parser import HTMLParser



class Course(models.Model):
    
    Class_File = models.FileField(upload_to='class_htmls')
    
    def __init__(self):
        models.Model.__init__(self)

    def create(self, file):
        self.Parser = MyHTMLParser()
        self.Parser.feed_file(file)
        self.Parser.sort_data_list('\t\t\t', '\t\t')
        course_info = self.Parser.data_list[0][1].split(' | ')
        self.code = course_info[2]
        self.term = course_info[0][11:]
        self.title = course_info[3][:-14]
        self.Students = []


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data_list = []
        self.tag_list = []

    def handle_starttag(self, tag, attrs):
        self.tag_list.append(tag)

    def handle_endtag(self, tag):
        self.tag_list.append(tag)

    def handle_data(self, data):
        if data not in ['\t', '\n']:
            self.data_list.append(data)        

    def feed_file(self, file_path):
        ofile = open(file_path, 'r')
        f = ofile.readlines()
        for line in f:
            self.feed(line)

    def print_data(self):
        for student in self.data_list:
            print(student)

    def sort_data_list(self, start_char, stop_char):
        # Sorts the data list compiling all of the data for each student into sperate lists
        new_data_list = []
        will_append = False
        for entry in self.data_list:
            if entry == start_char:
                will_append = True
                student = []
            elif entry == stop_char:
                if will_append == True:
                    new_data_list.append(student)
                will_append = False
            if will_append and entry is not start_char:
                student.append(entry)
        self.data_list = new_data_list


class Student(models.Model):

    pass