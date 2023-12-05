from django.db import models

from users.models import User
from quizes.models import Quiz

class Course(models.Model):
    classes = models.ManyToManyField("classes.Class", related_name='courses', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='courses/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    quiz = models.ManyToManyField(Quiz, related_name='courses', null=True, blank=True)


class CourseFile(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    file = models.FileField(upload_to='courses/')
