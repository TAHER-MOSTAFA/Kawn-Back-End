from collections import OrderedDict
from typing import List

from django.core.cache import cache
from graphene.types.scalars import Int, String

from chat.models import Message
from chat.tasks import update_dialog

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
        cls.__cache_dialog_last_msg(dialog_id=dialog_id, msg=msg)
        cls.__incr_users_msgs(users_ids, dialog_id)
        update_dialog(dialog_id)

    def _incr_users_msgs(users_ids, dialog_id):
        qs = cache.get_many(users_ids)
        for user_id in users_ids:
            if qs.get(user_id) == None:
                qs[user_id]["total_msgs"] = 1
                qs[user_id]["dialogs"] = OrderedDict(int)
            else:
                qs[user_id]["total_msgs"] += 1

            qs[user_id]["dialogs"][dialog_id] += 1
        cache.set_many(qs)

    def __cache_dialog_last_msg(dialog_id, msg) -> None:
        cache.set(f"{dialog_id}_lstmsg", msg)
