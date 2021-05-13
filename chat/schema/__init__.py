import graphene

from .mutation import SendChatMessage
from .query import Query
from .subscription import OnNewChatMessage


class Subscription(graphene.ObjectType):
    on_new_chat_message = OnNewChatMessage.Field()


class Mutation(graphene.ObjectType):

    send_chat_message = SendChatMessage.Field()
