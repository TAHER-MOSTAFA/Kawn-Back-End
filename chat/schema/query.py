import graphene
from graphql_jwt.decorators import login_required

from chat.models import Dialog, Message, UserMessage
from chat.utils import get_paginator

from .types import PaginatedMessageType, UserMessagesType


class Query(graphene.ObjectType):
    Dialog_message_history = graphene.Field(
        PaginatedMessageType,
        dialog_id=graphene.Int(),
        page=graphene.Int(),
        per_page=graphene.Int(),
    )
    UserUnseenMessages = graphene.List(UserMessagesType)

    @login_required
    def resolve_Dialog_message_history(self, info, dialog_id, page, per_page):
        if info.context.user not in Dialog.objects.get(id=dialog_id).users.all():
            raise Exception("NO permission")
        qs = Message.objects.filter(dialog_id=dialog_id).order_by("-time_date")
        return get_paginator(qs, per_page, page, PaginatedMessageType)

    @login_required
    def resolve_UserUnseenMessages(self, info):
        return UserMessage.objects.filter(user_id=info.context.user.id)
