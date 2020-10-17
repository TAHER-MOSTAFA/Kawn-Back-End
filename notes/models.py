from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()

class Note(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(user, related_name='notes', on_delete=models.CASCADE)
    