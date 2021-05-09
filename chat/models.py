from django.contrib.auth import get_user_model
from django.db import models

user = get_user_model()


class Dialog(models.Model):
    users = models.ManyToManyField(user)
    time_date = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    text = models.TextField()
    image = models.ImageField(null=True, blank=True)
    time_date = models.DateTimeField(auto_now_add=True)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)
    sender = models.ForeignKey(user, on_delete=models.CASCADE)
