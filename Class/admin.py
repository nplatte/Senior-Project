from django.contrib import admin
from .models import Course, Assignment
from django import forms
from django.conf import settings
from django.contrib.auth.models import User


class AssignmentAdmin(admin.ModelAdmin):


    list_display = ('title', 'course', 'due_date')
    ordering = ['course']
    list_filter = ('course', 'due_date')
    fields = (
        'course',
        'due_date',
        'title',
        'description'
    )
    
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course":
            course_list = Course.objects.filter(course_instructor=request.user)
            kwargs["queryset"] = course_list
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
        
        if db_field.name == "course_instructor":
            staff_list = User.objects.filter(is_staff=True) 


class CourseAdmin(admin.ModelAdmin):

    list_display = ('title', 'code', 'term')
    list_filter = ('term', 'code')
    fieldsets = (
        ('Course Information', {
            'fields': ('Class_File', 'title', 'code', 'term', 'course_instructor')
        }),
        ('Student Information', {
            'fields': ('students',)
        })
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(course_instructor=request.user)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "students":
            current_course = Course.objects.all().last()
            kwargs["queryset"] = current_course.students.all()
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course_instructor":
            staff_list = User.objects.filter(is_staff=True)
            kwargs["queryset"] = staff_list
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        self.obj = obj
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
                    'fields': ('title', 'code', 'term', 'course_instructor')
                }),
                ('Student Information', {
                'fields': ('students',)
                }),
            )
        return fieldsets
        
admin.site.register(Course, CourseAdmin)
admin.site.register(Assignment, AssignmentAdmin)
