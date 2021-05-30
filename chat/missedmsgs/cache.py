from collections import defaultdict
from typing import List

from django.core.cache import cache
from graphene.types.scalars import Int, String

from chat.models import Message
from chat.schema.types import PaginatedMessageType
from chat.tasks import update_dialog
from chat.utils import get_paginator

""""
user -> dict
user = {
    total_msgs : int
    dialogs: {
        dialog_id : int
    }
}
"""


class MissedMsgs:
    @classmethod
    def new_msg(cls, users_ids: List, dialog_id: Int, msg: String):
        users_ids.remove(msg.sender_id)
        cls.__cache_dialog_last_msg(dialog_id=dialog_id, msg=msg)
        cls.__incr_users_msgs(users_ids, dialog_id)
        update_dialog.apply_async(args=(dialog_id,))

    def __incr_users_msgs(users_ids, dialog_id):
        qs = cache.get_many(users_ids)
        for user_id in users_ids:
            if qs.get(user_id) == None:
                qs[user_id] = dict()
                qs[user_id]["total_msgs"] = 1
                qs[user_id]["dialogs"] = defaultdict(int)
            else:
                qs[user_id]["total_msgs"] += 1

            qs[user_id]["dialogs"][dialog_id] += 1
        cache.set_many(qs)

    def __cache_dialog_last_msg(dialog_id, msg) -> None:
        cache.set(f"{dialog_id}_lstmsg", msg)
