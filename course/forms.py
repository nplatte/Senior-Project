from django import forms
from course.models import Course
from django.core.exceptions import ValidationError
from html.parser import HTMLParser
from os import getcwd


class CourseModelFileForm(forms.ModelForm):  
    class Meta:
        model = Course
        fields = ['source_file']
        widgets = {
            'source_file' : forms.FileInput(
                attrs={
                    'class' : 'file_upload',
                    'id' : 'source_file_input'
                }
            )
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser = MyHTMLParser()

    def clean_source_file(self):
        file = self.cleaned_data['source_file']
        if file.name[-4:] == '.xls':
            return file
        raise ValidationError('source file is not .xls file')
    
    def save(self, *args, **kwargs):
        new_course = super().save(*args, **kwargs)
        course_info = self._get_course_info(new_course)
        new_course.title = course_info[4]
        new_course.term = f'{course_info[1]} {course_info[2]}'
        new_course.code = course_info[3]
        new_course.year = int(course_info[0])
        new_course.save()
        return new_course 

    def _get_course_info(self, course):
        file_path = f'{getcwd()}\\{course.source_file.name}'
        self.parser.feed_file(file_path)
        self.parser.sort_data_list('\t\t\t', '\t\t')
        rough = self.parser.data_list[0][1].split(' | ')
        term = rough[0].split(' ')
        title = rough[-1].split(' (')
        return term[2:5] + [rough[2]] + [title[0]]
    

class EditCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'code', 'term', 'year']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'id': 'edit-course-title'
                }
            ),
            'code': forms.TextInput(
                attrs={
                    'id': 'edit-course-code'
                }
            ),
            'term': forms.TextInput(
                attrs={
                    'id': 'edit-course-term'
                }
            )
        }

    def clean_year(self):
        year = self.cleaned_data['year']
        splt_yr = year.split('-')
        if 1000 < int(splt_yr[0]) < 9000 and 1000 < int(splt_yr[0]) < 9000:
            return year
        raise ValidationError(f'year {year} must be in format of YYYY-YYYY. Ex: 2023-2024')

    def clean_term(self):
        term = self.cleaned_data['term']
        accepted = [
            'Summer Term',
            'Fall Term',
            'May Term',
            'Winter Term',
        ]
        if term in accepted:
            return term
        raise ValidationError(f'Term {term} not in {accepted}')


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data_list = []
        self.tag_list = []

    def handle_data(self, data):
        # removes tabs and new line charecters from the data list
        if data not in ['\t', '\n']:
            self.data_list.append(data)        

    def feed_file(self, file_path):
        # works through file line by line
        ofile = open(file_path, 'r')
        f = ofile.readlines()
        for line in f:
            self.feed(line)

    def sort_data_list(self, start_char='\t\t\t', stop_char='\t\t'):
        # Take a start and end charecter and parses through data, returning a list of everything between the charecters,
        # returns a list if lists if there are multiple start and stops through the list
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