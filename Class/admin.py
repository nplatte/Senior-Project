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

    fields = ['Class_File', 'title', 'code', 'term']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.create()

    '''def add_view(self, request, extra_content=None):
        self.fields = ('Class_File')
        return super(CourseAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
         self.fields = ('Class_File', 'title', 'code', 'term')
         return super(CourseAdmin,self).change_view(request,object_id)'''

    def get_fields(self, request, obj=None):
        if not obj:
            fields=('Class_File',)
        else:
            fields =('term', 'title', 'code')
        return fields

    '''def get_form(self, request, obj=None, **kwargs):
        
        if obj: 
            kwargs['fields'] = ['Class_File', 'title', 'term', 'code']
        else:
            kwargs['fields'] = ['Class_File', 'title', 'term', 'code']
        return super(CourseAdmin, self).get_form(request, obj, **kwargs)'''
        
    
        
        
        

admin.site.register(Course, CourseAdmin)
