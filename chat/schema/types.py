import graphene
from graphene_django import DjangoObjectType

from chat.models import *


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
