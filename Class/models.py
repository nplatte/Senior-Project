from django.db import models
from html.parser import HTMLParser



class Course(models.Model):
    
    Class_File = models.FileField(upload_to='class_htmls')


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
        print(self.data_list)

    def sort_data_list(self, start_char, stop_char):
        new_list = []
        append = False
        for entry in self.data_list:
            if entry == start_char:
                append = True
            elif entry == stop_char:
                append = False
            if append and entry is not start_char:
                new_list.append(entry)
        return new_list