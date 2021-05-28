from django.db.models import Manager


class DialogManager(Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related("users")


class UserMessageManager(Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("message")
