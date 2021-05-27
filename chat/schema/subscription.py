import channels_graphql_ws
import graphene
from graphql_jwt.decorators import login_required

from chat.models import Dialog


class OnNewChatMessage(channels_graphql_ws.Subscription):
    dialog = graphene.Int()
    text = graphene.String()

    class Arguments:
        None

    @login_required
    def subscribe(self, info, dialog=None):
        dialogs = Dialog.objects.filter(users__id=info.context.user.id)
        return [str(dialog.id) for dialog in dialogs]

    def publish(self, info):
        new_msg_dialog = self["dialog"]
        new_msg_text = self["text"]

        return OnNewChatMessage(dialog=new_msg_dialog, text=new_msg_text)

    @classmethod
    def new_chat_message(cls, dialog, text):
        cls.broadcast(group=str(dialog), payload={"dialog": dialog, "text": text})


class Subscription(graphene.ObjectType):
    on_new_chat_message = OnNewChatMessage.Field()
