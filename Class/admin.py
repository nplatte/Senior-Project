from django.contrib import admin
from .models import Course
from django import forms

class CourseAdminModelForm(forms.ModelForm):

    class Meta:

        model = Course
        
        fields = [
            'Class_File', 'title', 'code', 'term'
        ] 

class CourseAdmin(admin.ModelAdmin):

    form = CourseAdminModelForm

    fieldsets = (
        ('Course Information', {
            'fields': ('Class_File', 'title', 'code', 'term')
        }),
    )

    #fields = ['Class_File', 'title', 'code', 'term']

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
            #fields = ('Class_File',)
        else:
            fieldsets = (
                ('Course Information', {
                    'fields': ('title', 'code', 'term')
                }),
            )
            #fields = ('title', 'code', 'term')
        return fieldsets
        
admin.site.register(Course, CourseAdmin)
