import os

import channels
import channels_graphql_ws
import django
from channels.auth import AuthMiddlewareStack, get_user
from django.core.asgi import get_asgi_application

from .cache_utils import cache_clear_userstate, cache_user_is_online


from .schema import schema


class GraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
    schema = schema

    async def on_connect(self, payload):
        self.scope["user"] = await get_user(self.scope)
        cache_user_is_online(self.scope["user"].pk)
        super().on_connect(payload)

    async def disconnect(self, code):
        cache_clear_userstate(self.scope["user"].pk)
        super().disconnect(code)




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
