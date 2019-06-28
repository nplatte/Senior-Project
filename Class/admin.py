from django.contrib import admin
from .models import Course

class CourseAdmin(admin.ModelAdmin):
    fields = ['Class_File']

admin.site.register(Course, CourseAdmin)
