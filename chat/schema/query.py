import graphene
from django.core.cache import cache
from graphql_jwt.decorators import login_required

from chat.missedmsgs.cache import MissedMsgs
from chat.models import Dialog, Message, UserMessage
from chat.permissions import UserInDialog
from chat.utils import CacheUsersMsgs, get_paginator

from .types import DialogType, MessageType, PaginatedMessageType, UnseenMsgsType


class Query(graphene.ObjectType):
    Dialog_message_history = graphene.Field(
        PaginatedMessageType,
        dialog_id=graphene.Int(),
        page=graphene.Int(required=False, default_value=1),
        per_page=graphene.Int(required=False, default_value=20),
    )
    UserUnseenMessages = graphene.Field(UnseenMsgsType)
    # MarkDialogSeen = graphene.Boolean(Name="ok",dialog_id=graphene.Int())

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
    def resolve_UserUnseenMessages(self, info):
        return UnseenMsgsType()
