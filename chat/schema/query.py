import graphene
from django.core.cache import cache
from graphql_jwt.decorators import login_required

from chat.missedmsgs.cache import MissedMsgs
from chat.models import Dialog, Message, UserMessage
from chat.permissions import UserInDialog
from chat.utils import CacheUsersMsgs, get_paginator

from .types import PaginatedDialogType, PaginatedMessageType



class Query(graphene.ObjectType):
    Dialog_message_history = graphene.Field(
        PaginatedMessageType,
        dialog_id=graphene.Int(),
        page=graphene.Int(required=False, default_value=1),
        per_page=graphene.Int(required=False, default_value=20),
    )
    UserDialogs = graphene.Field(
        PaginatedDialogType,
        page=graphene.Int(required=False, default_value=1),
        per_page=graphene.Int(required=False, default_value=10),
    )

    TotalUnseenMsgs = graphene.Int()

    @login_required
    def resolve_Dialog_message_history(self, info, dialog_id, page, per_page):
        UserInDialog(info, dialog_id)

        qs = Message.objects.filter(dialog_id=dialog_id)
        try:
            c_user = cache.get(info.context.user.id)
            dialog_msgs = c_user.get("dialogs").get(dialog_id)
        except:
            dialog_msgs = 0

        if page and dialog_msgs == 0:
            pass
        else:
            c_user["total_msgs"] = max(0, c_user["total_msgs"] - per_page)

            c_user["dialogs"][dialog_id] = max(
                0, c_user["dialogs"][dialog_id] - per_page
            )
            cache.set(info.context.user.id, c_user)

            page = max(1, dialog_msgs / per_page)

        return get_paginator(qs, per_page, page, PaginatedMessageType)

    @login_required
    def resolve_UserDialogs(self, info, page, per_page):
        usr_msg = cache.get(info.context.user.id)
        if usr_msg:
            dialog_ids = usr_msg.get("dialogs").keys()
            qs = Dialog.objects.filter(pk__in=dialog_ids).order_by("-last_sent")
        qs = info.context.user.dialog_set.order_by("-last_sent")

        return get_paginator(qs, per_page, page, PaginatedDialogType)

    @login_required
    def resolve_TotalUnseenMsgs(self, info):
        try:
            return cache.get(info.context.user.id).get("total_msgs")
        except:
            return 0
