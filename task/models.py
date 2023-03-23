from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    completed = models.BooleanField(default=False, blank=False, null=False)
    due_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.title
