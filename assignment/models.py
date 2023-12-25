from django.db import models
from course.models import Course

class Assignment(models.Model):
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, related_name='assignments')
    title = models.CharField(max_length=50, default='')
    description = models.TextField(default='')
    due_date = models.DateTimeField(blank=True, null=True)
    display_date = models.DateTimeField(blank=True, null=True)

    def __repr__(self) -> str:
        return str(self.title)