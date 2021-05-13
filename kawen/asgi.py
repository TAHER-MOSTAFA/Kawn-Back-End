import os

import channels
import channels_graphql_ws
import django
from channels.auth import AuthMiddlewareStack, get_user
from django.core.asgi import get_asgi_application

from .schema import schema


class GraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
    schema = schema

    async def on_connect(self, payload):
        self.scope["user"] = await get_user(self.scope)
        print(f"{self.scope['user'] } connected")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kawen.settings")


application = channels.routing.ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(
            channels.routing.URLRouter(
                [django.urls.path("graphql/", GraphqlWsConsumer.as_asgi())]
            )
        )
    }
)
