from django.db import models
from django.conf import settings
from Class.models import Course, Assignment

class HomeworkSubmission(models.Model):

    homework = models.FileField(upload_to='handouts')
    course = models.ForeignKey(Course, on_delete = models.SET_NULL, null = True)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.SET_NULL, null = True)
    assignment = models.ForeignKey(Assignment, on_delete = models.SET_NULL, null = True)

    def __str__(self):
        return self.student
