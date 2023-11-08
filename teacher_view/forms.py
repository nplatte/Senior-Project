from django import forms
from django import forms
from teacher_view.models import Course
from django.core.exceptions import ValidationError

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

    def clean_Class_File(self):
        file = self.data['Class_File']
        if file.name[-4:] == '.xls':
            return file
        raise ValidationError('file is not .xls file')