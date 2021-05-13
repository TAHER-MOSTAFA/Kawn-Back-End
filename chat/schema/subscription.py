import channels_graphql_ws
import graphene
from graphql_jwt.decorators import login_required

from chat.models import Dialog


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
