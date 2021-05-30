from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

from .managers import DialogManager, UserMessageManager

User = get_user_model()


class Dialog(models.Model):
    users = models.ManyToManyField(User)
    time_date = models.DateTimeField(auto_now_add=True)
    last_sent = models.DateTimeField(default=datetime.now)

    objects = DialogManager()

    objects = DialogManager()


class Message(models.Model):
    text = models.TextField()
    image = models.ImageField(null=True, blank=True)
    time_date = models.DateTimeField(auto_now_add=True)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-time_date",)


class UserMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    objects = UserMessageManager()
