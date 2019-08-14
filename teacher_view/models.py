from django.db import models

class Grade(models.Model):

    student = models.ForeignKey('Class.Student', models.CASCADE, null=True)
    course = models.ForeignKey('Class.Course', models.CASCADE, null=True)
    catagories = models.CharField(default='', max_length=200)
    student_scores = models.CharField(default='', max_length=200)
    points_possible = models.CharField(default='', max_length=200)
    letter_grade = models.CharField(default='', max_length=5)

    def parse_file(self):
        pass