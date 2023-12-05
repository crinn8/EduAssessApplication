from django.db import models

from users.models import User
from quizes.models import Quiz

class Class(models.Model):
    students = models.ManyToManyField(User, related_name='classes', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
