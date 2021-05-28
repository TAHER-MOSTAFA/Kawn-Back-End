import re
from sys import argv
from typing import List

from django.core.cache import caches
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models.query import QuerySet

from .models import Message, User, UserMessage
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
    # "user.id_msg.id" -> msg.id
    cache = caches["default"]

    @classmethod
    def new_message(cls, msg: Message, dialog_users: QuerySet) -> None:
        users_ids = [user.id for user in dialog_users.exclude(id=msg.sender_id)]
        cls.__write_to_cache(msg, users_ids)
        cls.__write_async_db(msg.id, users_ids)

    @classmethod
    def __write_to_cache(cls, msg: Message, users_ids: List) -> None:
        users_message = {f"{user_id}_{msg.id}": msg for user_id in users_ids}
        cls.cache.set_many(users_message)

    @classmethod
    def get_user_missed_msgs(cls, user_id) -> QuerySet:
        msgs = cls.__fetch_cached_user_msgs(user_id)

        if len(msgs) == 0:
            msgs = cls.__fetch_user_messages_from_db(user_id)
        return msgs

    @classmethod
    def __fetch_cached_user_msgs(cls, user_id) -> List[Message]:
        return cls.cache.keys(f"{user_id}_**")

    @classmethod
    def __fetch_user_messages_from_db(cls, user_id) -> List[Message]:
        return list(Message.objects.filter(usermessage__user_id=user_id))

    def __write_async_db(msg_id, users_ids) -> None:
        write_user_missed_messages_to_db.apply_async(args=(msg_id, users_ids))

    @classmethod
    def msg_seen(cls, user_id, msg_id) -> None:
        cls.cache.delete(f"{user_id}_{msg_id}")
