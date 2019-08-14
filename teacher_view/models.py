from django.db import models
from Class.models import Student, Course

class Grade(models.Model):

    student = models.ManyToManyField(Student)
    course = models.ManyToManyField(Course)
    grade_file = models.FileField(upload_to='course_grades')
    letter_grade = models.CharField(default='', max_length=5)

    def parse_grade_file(self):
        pass
