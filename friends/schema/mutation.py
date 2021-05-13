import graphene
from django.shortcuts import get_object_or_404
from friendship.models import Friend, FriendshipRequest
from graphql_jwt.decorators import login_required

from users.models import Member

from .types import FriendRequesType


class SendFriendRequest(graphene.Mutation):
    request = graphene.Field(FriendRequesType)

    class Arguments:
        other_user_id = graphene.Int()

    def mutate(self, info, other_user_id, *args, **kwargs):
        other_user = get_object_or_404(Member, id=other_user_id)
        request = Friend.objects.add_friend(info.context.user, other_user)
        return SendFriendRequest(request)


class AcceptFriendRequest(graphene.Mutation):
    accepted = graphene.Boolean()

    class Arguments:
        request_id = graphene.Int()

    def mutate(self, info, request_id, *args, **kwargs):
        request = get_object_or_404(FriendshipRequest, pk=request_id)
        return AcceptFriendRequest(request.accept())


class RejectFriendRequest(graphene.Mutation):
    rejected = graphene.Boolean()

    class Arguments:
        request_id = graphene.Int()

    def mutate(self, info, request_id, *args, **kwargs):
        request = get_object_or_404(FriendshipRequest, pk=request_id)
        return AcceptFriendRequest(request.reject())


class RemoveFriend(graphene.Mutation):
    removed = graphene.Boolean()

    class Arguments:
        other_user_id = graphene.Int()

    def mutate(self, info, other_user_id, *args, **kwargs):
        other_user = get_object_or_404(Member, id=other_user_id)
        request = Friend.objects.remove_friend(info.context.user, other_user)
        return RemoveFriend(True)
