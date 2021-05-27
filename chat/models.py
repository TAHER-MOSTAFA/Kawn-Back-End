from django.contrib.auth import get_user_model
from django.db import models

from .managers import DialogManager, UserMessageManager

User = get_user_model()


class Dialog(models.Model):
    users = models.ManyToManyField(User)
    time_date = models.DateTimeField(auto_now_add=True)

    objects = DialogManager()


class Message(models.Model):
    text = models.TextField()
    image = models.ImageField(null=True, blank=True)
    time_date = models.DateTimeField(auto_now_add=True)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Message, self).save(*args, **kwargs)

        users = self.dialog.users.exclude(id=self.sender_id)

        UserMessage.objects.bulk_create(
            [UserMessage(user_id=user.id, message_id=self.id) for user in users]
        )


class UserMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    objects = UserMessageManager()
