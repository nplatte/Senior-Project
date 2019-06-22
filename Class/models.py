from django.db import models

class Course(models.Model):

    title = models.CharField(default='', max_length = 70, help_text = 'Class name')
    professor = models.CharField(default = '', max_length = 30, help_text = 'Course Instructor')
