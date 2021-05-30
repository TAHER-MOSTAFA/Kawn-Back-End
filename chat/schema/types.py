import graphene
from django.core.cache import cache
from django.db.models import fields
from django.db.models.base import Model
from graphene_django import DjangoObjectType

from chat.models import *
from chat.utils import get_paginator


class MessageType(DjangoObjectType):
    class Meta:
        model = Message


class PaginatedMessageType(graphene.ObjectType):
    page = graphene.Int()
    total_pages = graphene.Int()
    has_next = graphene.Boolean()
    messages = graphene.List(MessageType)


class DialogType(DjangoObjectType):
    unseen_msgs = graphene.Field(PaginatedMessageType)

    class Meta:
        model = Dialog

    def resolve_unseen_msgs(self, info):
        num = cache.get(info.context.user.id).get("dialogs").get(self.id) or 0
        if not num:
            return None
        qs = Message.objects.filter(dialog_id=self.id)
        c_user = cache.get(info.context.user.id)
        c_user["total_msgs"] -= 10
        c_user["dialogs"][self.id] -= 10
        cache.set(info.context.user.id, c_user)
        return get_paginator(
            qs=qs, page_size=10, page=int(num / 10), paginated_type=PaginatedMessageType
        )


"""
{
    total : 1
    dialogs : [
        {
            unseen_num : 1
            last_msg : Message
            unseen_messages: {
                has_next
                msg[
                    id : 1
                    text : "I'm message"
                ]
            }
        }
    ]
}
"""


class SimpleDialogType(DjangoObjectType):
    unseen_num = graphene.Int()
    last_msg = graphene.Field(MessageType)

    class Meta:
        model = Dialog
        fields = ["id", "last_sent"]

    def resolve_unseen_num(self, info):
        try:
            return cache.get(info.context.user.id).get("dialogs").get(self.id)
        except:
            return None

    def resolve_last_msg(self, info):
        return cache.get(f"{self.id}_lstmsg")


class PaginatedDialogType(graphene.ObjectType):
    page = graphene.Int()
    total_pages = graphene.Int()
    has_next = graphene.Boolean()
    dialog = graphene.List(SimpleDialogType)
