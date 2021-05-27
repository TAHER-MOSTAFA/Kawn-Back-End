import graphene
from graphql_jwt.decorators import login_required

from chat.models import Dialog, Message, UserMessage

from .subscription import OnNewChatMessage


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


class MarkMessageSeen(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        user_message_id = graphene.Int()

    @login_required
    def mutate(self, info, user_message_id):
        obj = UserMessage.objects.get(id=user_message_id)
        if obj.user_id != info.context.user.id:
            raise Exception("NO permission")

        UserMessage.objects.get(id=user_message_id).delete()
        return MarkMessageSeen(ok=True)


class Mutation(graphene.ObjectType):
    Send_chat_message = SendChatMessage.Field()
    Mark_message_seen = MarkMessageSeen.Field()
