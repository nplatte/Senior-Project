from django.contrib import admin
from .models import Course

class CourseAdmin(admin.ModelAdmin):
    fields = ['Class_File']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.create()
        
        
        
        
        

admin.site.register(Course, CourseAdmin)
