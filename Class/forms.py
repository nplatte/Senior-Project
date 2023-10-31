from django.forms import ModelForm
from Class.models import Course

class CourseModelForm(ModelForm):

    class Meta:
        model = Course
        fields = ['Class_File']