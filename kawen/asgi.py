import os

import channels
import channels_graphql_ws
import django

from .schema import schema


class GraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
    schema = schema

    async def on_connect(self, payload):
        self.scope["user"] = await channels.auth.get_user(self.scope)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kawen.settings")


application = channels.routing.ProtocolTypeRouter(
    {
        "websocket": channels.auth.AuthMiddlewareStack(
            channels.routing.URLRouter(
                [django.urls.path("graphql/", GraphqlWsConsumer)]
            )
        )
    }
)
