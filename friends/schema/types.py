from friendship.models import FriendshipRequest
from graphene_django import DjangoObjectType


class FriendRequesType(DjangoObjectType):
    class Meta:
        model = FriendshipRequest
        exclude = [
            "viewed",
        ]
