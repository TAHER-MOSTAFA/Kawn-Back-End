import graphene
from django.core.cache import cache
from graphql_jwt.decorators import login_required

from chat.models import Dialog, Message, UserMessage
from chat.utils import CacheUsersMsgs, get_paginator

from .types import MessageType, PaginatedMessageType


class Query(graphene.ObjectType):
    Dialog_message_history = graphene.Field(
        PaginatedMessageType,
        dialog_id=graphene.Int(),
        page=graphene.Int(),
        per_page=graphene.Int(),
    )
    UserUnseenMessages = graphene.Field(
        PaginatedMessageType,
        page=graphene.Int(),
        per_page=graphene.Int(),
    )

    @login_required
    def resolve_Dialog_message_history(self, info, dialog_id, page, per_page):
        if info.context.user not in Dialog.objects.get(id=dialog_id).users.all():
            raise Exception("NO permission")
        qs = Message.objects.filter(dialog_id=dialog_id).order_by("-time_date")
        return get_paginator(qs, per_page, page, PaginatedMessageType)

    @login_required
    def resolve_UserUnseenMessages(self, info, page, per_page):
        qs = CacheUsersMsgs.get_user_missed_msgs(user_id=info.context.user.id)
        return get_paginator(qs, per_page, page, PaginatedMessageType, len(qs))
