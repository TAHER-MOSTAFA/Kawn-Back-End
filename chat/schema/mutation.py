import graphene
from django.core.cache import cache
from graphql_jwt.decorators import login_required

from chat.missedmsgs.cache import MissedMsgs
from chat.models import Dialog, Message, UserMessage
from chat.utils import CacheUsersMsgs

from .subscription import OnNewChatMessage


class SendChatMessage(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        dialog_id = graphene.Int()
        text = graphene.String()

    @login_required
    def mutate(self, info, dialog_id, text):
        dialog_users = CacheUsersMsgs.get_dialog_get_or_set(dialog_id)
        if info.context.user.id not in dialog_users:
            raise Exception("NO permission")

        msg = Message.objects.create(
            text=text, sender=info.context.user, dialog_id=dialog_id
        )
        MissedMsgs.new_message(dialog_users, dialog_id, msg)
        OnNewChatMessage.new_chat_message(dialog=dialog_id, text=text)

        return SendChatMessage(ok=True)


class MarkMessageSeen(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        user_message_id = graphene.Int()

    @login_required
    def mutate(self, info, message_id):
        CacheUsersMsgs.msg_seen(msg_id=message_id, user_id=info.context.user_id)
        return MarkMessageSeen(ok=True)


class Mutation(graphene.ObjectType):
    Send_chat_message = SendChatMessage.Field()
    Mark_message_seen = MarkMessageSeen.Field()
