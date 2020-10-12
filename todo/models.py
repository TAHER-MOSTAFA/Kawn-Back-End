from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()

class TaskCard(models.Model):
    name = models.CharField(max_length=40)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    num = models.PositiveSmallIntegerField(default=0,editable=False)
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name='TaskCards')

class Task(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True,blank=True)
    done = models.BooleanField(default=False)
    taskcard = models.ForeignKey(TaskCard, on_delete=models.CASCADE, related_name='task')