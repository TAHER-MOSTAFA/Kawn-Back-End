import graphene

from .mutation import (AcceptFriendRequest, RejectFriendRequest, RemoveFriend,
                       SendFriendRequest)
from .query import Query


class Mutation(graphene.ObjectType):
    SendFriendRequest = SendFriendRequest.Field()
    RemoveFriend = RemoveFriend.Field()
    RejectFriendRequest = RejectFriendRequest.Field()
    AcceptFriendRequest = AcceptFriendRequest.Field()
