from django import forms
from django import forms
from teacher_view.models import Course
from django.core.exceptions import ValidationError
from html.parser import HTMLParser


class CourseModelForm(forms.ModelForm):  
    class Meta:
        model = Course
        fields = ['Class_File']
        widgets = {
            'Class_File' : forms.FileInput(
                attrs={
                    'class' : 'file_upload',
                    'id' : 'class_file'
                }
            )
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.parser = MyHTMLParser()

    def clean_Class_File(self):
        file = self.cleaned_data['Class_File']
        if file.name[-4:] == '.xls':
            return file
        raise ValidationError('file is not .xls file')
    

    '''def _get_course_info(self):
        file = self.data['file']
        self.parser.feed_file(file)
        self.parser.sort_data_list('\t\t\t', '\t\t')
        rough = self.parser.data_list[0][1].split(' | ')
        term = rough[0].split(' ')
        title = rough[-1].split(' (')
        return term[2:5] + [rough[2]] + [title[0]]

    def assign_course_info(self):
        info = self._get_course_info()
        course = Course.objects.create(title=info[4], term=f'{info[1]} {info[2]}', code=info[3], year=int(info[0]))
        return course'''
    

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