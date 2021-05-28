from kawen.celery import app

from .models import UserMessage


@app.task
def write_user_missed_messages_to_db(msg_id, users_ids):
    UserMessage.objects.bulk_create(
        [UserMessage(user_id=user_id, message_id=msg_id) for user_id in users_ids]
    )
