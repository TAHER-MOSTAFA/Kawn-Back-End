import graphene
from django.core.cache import cache
from graphql_jwt.decorators import login_required

from chat.missedmsgs.cache import MissedMsgs
from chat.models import Dialog, Message, UserMessage
from chat.permissions import UserInDialog

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
        MissedMsgs.new_msg(dialog_users, dialog_id, msg)
        OnNewChatMessage.new_chat_message(dialog=dialog_id, text=text)

        return SendChatMessage(ok=True)


class MarkDialogSeen(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        dialog_id = graphene.Int()

    @login_required
    def mutate(self, info, dialog_id):
        UserInDialog(info, dialog_id)

        try:
            c_user = cache.get(info.context.user.id)
            dialog_msgs = c_user.get("dialogs").get(dialog_id)
            c_user["total_msgs"] = max(0, c_user["total_msgs"] - dialog_msgs)
            c_user["dialogs"][dialog_id] = 0
            cache.set(info.context.user.id, c_user)
        except:
            pass
        return True



class Mutation(graphene.ObjectType):
    Send_chat_message = SendChatMessage.Field()
    Mark_dialog_seen = MarkDialogSeen.Field()
