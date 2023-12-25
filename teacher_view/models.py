from django.db import models
from course.models import Course


class Assignment(models.Model):
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=50, default='')
    description = models.TextField(default='')
    due_date = models.DateTimeField(blank=True, null=True)
    display_date = models.DateTimeField(blank=True, null=True)

    def __repr__(self) -> str:
        return str(self.title)


class Handout(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=25, default='')
    handout = models.FileField()
    post_date = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.title


class Grade(models.Model):

    student = models.ForeignKey('course.Student', models.CASCADE, null=True)
    course = models.ForeignKey('course.Course', models.CASCADE, null=True)
    catagories = models.CharField(default='', max_length=200)
    student_scores = models.CharField(default='', max_length=200)
    points_possible = models.CharField(default='', max_length=200)
    letter_grade = models.CharField(default='', max_length=5)

    def __str__(self):
        return self.student.name