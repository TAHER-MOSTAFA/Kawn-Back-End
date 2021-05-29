from django.core.cache import cache

from kawen.celery import app

from .models import Message, UserMessage



@app.task
def write_user_missed_messages_to_db(msg_id, users_ids):

    qs = cache.get_many(users_ids)
    msg = Message.objects.get(id=msg_id)
    UserMessage.objects.bulk_create(
        [
            UserMessage(user_id=user_id, message_id=msg_id)
            for user_id in users_ids
            if msg in qs.get(user_id)
        ]
    )
