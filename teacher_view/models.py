from django.db import models
from course.models import Course


class Handout(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=25, default='')
    handout = models.FileField()
    post_date = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.title