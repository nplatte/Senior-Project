from django import forms
from django.forms import ModelForm
from teacher_view.models import Course
from django.core.exceptions import ValidationError

class CourseModelForm(ModelForm):

    class Meta:
        model = Course
        fields = ['Class_File']
        widgets = {
            'file' : forms.FileInput(
                attrs={
                    'class' : 'file_upload',
                    'id' : 'class_file'
                }
            )
        }

    def clean_Class_File(self):
        file = self.cleaned_data['Class_File']
        if file.name[-4:] == '.xls':
            return file
        raise ValidationError('file is not .xls file')