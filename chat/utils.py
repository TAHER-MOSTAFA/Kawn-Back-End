import re
from sys import argv
from typing import List

from django.core.cache import caches
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models.query import QuerySet

from .models import Dialog, Message, User, UserMessage
from .tasks import write_user_missed_messages_to_db


def get_paginator(qs, page_size, page, paginated_type, **kwargs):
    p = Paginator(qs, page_size)
    try:
        page_obj = p.page(page)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    return paginated_type(
        page=page_obj.number,
        total_pages=p.num_pages,
        has_next=page_obj.has_next(),
        messages=page_obj.object_list,
        **kwargs,
    )


class CacheUsersMsgs:
    # key -> value
    # user.id -> {  "total_msgs" :
    #               dialog_id : List[Message]
    # }
    cache = caches["default"]

    @classmethod
    def new_message(cls, msg: Message, dialog_users: List[int]) -> None:
        (users_ids := dialog_users).remove(msg.sender_id)
        cls.__write_to_cache(msg, users_ids)
        cls.__write_async_db(msg.id, users_ids)

    @classmethod
    def __write_to_cache(cls, msg: Message, users_ids: List) -> None:
        qs = cls.cache.get_many(users_ids)
        for user_id in users_ids:
            if qs.get(user_id) != None:
                qs.get(user_id).append(msg)
            else:
                qs[user_id] = [msg]
        cls.cache.set_many(qs)

    @classmethod
    def get_user_missed_msgs(cls, user_id) -> QuerySet:
        msgs = cls.__fetch_cached_user_msgs(user_id)

        if not msgs:
            msgs = cls.__fetch_user_messages_from_db(user_id)
        return msgs

    @classmethod
    def __fetch_cached_user_msgs(cls, user_id) -> List[Message]:
        return cls.cache.get(user_id)

    @classmethod
    def __fetch_user_messages_from_db(cls, user_id) -> List[Message]:
        return list(Message.objects.filter(usermessage__user_id=user_id))

    def __write_async_db(msg_id, users_ids) -> None:
        write_user_missed_messages_to_db.apply_async(
            args=(msg_id, users_ids),
        )

    @classmethod
    def msg_seen(cls, user_id, msg_id) -> None:
        q = cls.cache.get(user_id)
        msg = Message.objects.get(pk=msg_id)
        q.remove(msg)
        UserMessage.objects.filter(message_id=msg_id, user_id=user_id).delete()

    @classmethod
    def get_dialog_get_or_set(cls, dialog_id):
        dialog = cls.cache.get(f"{dialog_id}_dUsers")
        if dialog == None:
            dialog_users = Dialog.objects.get(id=dialog_id).users.all()
            dialog = [user.id for user in dialog_users]
            cls.cache.set(f"{dialog_id}_dialog", dialog)
        return dialog
