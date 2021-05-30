import graphene
from django.core.cache import cache
from graphql_jwt.decorators import login_required

from chat.missedmsgs.cache import MissedMsgs
from chat.models import Dialog, Message, UserMessage
from chat.utils import CacheUsersMsgs, get_paginator

from .types import MessageType, PaginatedMessageType, UnseenMsgsType


class Query(graphene.ObjectType):
    Dialog_message_history = graphene.Field(
        PaginatedMessageType,
        dialog_id=graphene.Int(),
        page=graphene.Int(),
        per_page=graphene.Int(),
    )
    UserUnseenMessages = graphene.Field(UnseenMsgsType)
    UserDialogUnseenMessages = graphene.Field(
        PaginatedMessageType, dialog_id=graphene.Int()
    )

    @login_required
    def resolve_Dialog_message_history(self, info, dialog_id, page, per_page):
        if info.context.user.id not in CacheUsersMsgs.get_dialog_get_or_set(dialog_id):
            raise Exception("NO permission")
        qs = Message.objects.filter(dialog_id=dialog_id).order_by("-time_date")
        return get_paginator(qs, per_page, page, PaginatedMessageType)

    @login_required
    def resolve_UserUnseenMessages(self, info):
        pass

    @login_required
    def UserDialogUnseenMessages(self, info, dialog_id):
        return Dialog(id=dialog_id)
