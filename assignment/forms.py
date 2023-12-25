from django import forms
from django import forms
from teacher_view.models import Assignment


class AssignmentForm(forms.ModelForm):

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'display_date', 'course']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'id': 'a-title-input'
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'id': 'a-description-input'
                }
            ),
            'due_date': forms.DateTimeInput(
                attrs={
                    'id': 'a-due-date-input'
                }
            ),
            'display_date': forms.DateTimeInput(
                attrs={
                    'id': 'a-display-date-input'
                }
            ),
            'course': forms.Select(
                attrs={
                    'id': 'a-course-input'
                }
            )
        }
    