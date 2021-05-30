from datetime import datetime

from django.core.cache import cache

from kawen.celery import app

from .models import Dialog, Message, UserMessage


@app.task
def update_dialog(
    dialog_id,
):
    Dialog.objects.filter(pk=dialog_id).update(last_sent=datetime.now())
