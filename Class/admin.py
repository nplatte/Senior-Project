from django.contrib import admin
from .models import Course
from django import forms

class CourseAdminModelForm(forms.ModelForm):

    class Meta:

        model = Course
        
        fields = [
            'Class_File', 'title', 'code', 'term', 'students'
        ] 

class CourseAdmin(admin.ModelAdmin):

    form = CourseAdminModelForm

    fieldsets = (
        ('Course Information', {
            'fields': ('Class_File', 'title', 'code', 'term')
        }),
        ('Student Information', {
            'fields': ('students',)
        })
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.create()

    def get_fieldsets(self, request, obj=None):
        if not obj:
            fieldsets = (
                ('Course Information', {
                    'fields': ('Class_File',)
                }),
            )
        else:
            fieldsets = (
                ('Course Information', {
                    'fields': ('title', 'code', 'term')
                }),
                ('Student Information', {
                'fields': ('students',)
                }),
            )
        return fieldsets
        
admin.site.register(Course, CourseAdmin)
