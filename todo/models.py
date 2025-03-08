from django.db import models

from django.contrib.auth.models import User

class Todo(models.Model):
    user = models.CharField(max_length=30)
    heading = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    marked = models.BooleanField()

    def __str__(self) -> str:
        return super().__str__()