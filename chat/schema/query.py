import graphene
from graphql_jwt.decorators import login_required

from chat.models import Dialog, Message
from chat.utils import get_paginator

from .types import PaginatedMessageType


class Query(graphene.ObjectType):
    Dialog_message_history = graphene.Field(
        PaginatedMessageType, dialog_id=graphene.Int(), page=graphene.Int()
    )

    @login_required
    def resolve_Dialog_message_history(self, info, dialog_id, page):
        if info.context.user not in Dialog.objects.get(id=dialog_id).users.all():
            raise Exception("NO permission")
        qs = Message.objects.filter(dialog_id=dialog_id).order_by("-time_date")
        return get_paginator(qs, 3, page, PaginatedMessageType)
