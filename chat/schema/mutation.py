import graphene
from graphql_jwt.decorators import login_required

from chat.models import Dialog, Message

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
