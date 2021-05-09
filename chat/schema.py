import channels_graphql_ws
import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from .models import *
from .utils import get_paginator


class MessageType(DjangoObjectType):
    class Meta:
        model = Message


class PaginatedMessageType(graphene.ObjectType):
    page = graphene.Int()
    total_pages = graphene.Int()
    has_next = graphene.Boolean()
    messages = graphene.List(MessageType)


class DialogType(DjangoObjectType):
    class Meta:
        model = Dialog


# --------------------------------------------------------QUERIES
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


# --------------------------------------------------------MUTATIONS
class SendChatMessage(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        dialog_id = graphene.Int()
        text = graphene.String()

    @login_required
    def mutate(self, info, dialog_id, text):
        if info.context.user not in Dialog.objects.get(id=dialog_id).users.all():
            raise Exception("NO permission")

        Message.objects.create(text=text, sender=info.context.user, dialog_id=dialog_id)

        OnNewChatMessage.new_chat_message(dialog=dialog_id, text=text)

        return SendChatMessage(ok=True)


class Mutation(graphene.ObjectType):

    send_chat_message = SendChatMessage.Field()


# ------------------------------------------------------------------------ SUBSCRIPTIONS


class OnNewChatMessage(channels_graphql_ws.Subscription):
    dialog = graphene.Int()
    text = graphene.String()

    class Arguments:
        dialog = graphene.Int()

    @login_required
    def subscribe(self, info, dialog=None):
        if info.context.user in Dialog.objects.get(id=dialog).users.all():
            return [str(dialog)]
        else:
            raise Exception("NO permission")

    def publish(self, info, dialog=None):
        new_msg_dialog = self["dialog"]
        new_msg_text = self["text"]

        return OnNewChatMessage(dialog=new_msg_dialog, text=new_msg_text)

    @classmethod
    def new_chat_message(cls, dialog, text):
        cls.broadcast(group=str(dialog), payload={"dialog": dialog, "text": text})


class Subscription(graphene.ObjectType):
    on_new_chat_message = OnNewChatMessage.Field()
