import graphene
from django.shortcuts import get_object_or_404
from friendship.models import Friend, FriendshipRequest
from graphql_jwt.decorators import login_required

from users.models import Member
from users.schema import MemberType

from .types import FriendRequesType


class Query(graphene.ObjectType):
    Friends_list = graphene.List(MemberType)
    IsFriend = graphene.Boolean(other_user_id=graphene.Int())
    FriendRequests = graphene.List(FriendRequesType)
    NumberOfFriendRequests = graphene.Int()
    RequestSent = graphene.Boolean()

    @login_required
    def resolve_Friends_list(self, info):
        return Friend.objects.friends(info.context.user)

    @login_required
    def resolve_IsFriend(self, info, other_user_id):
        other_user = get_object_or_404(Member, id=other_user_id)
        return Friend.objects.are_friends(info.context.user, other_user) == True

    @login_required
    def resolve_FriendRequests(self, info):
        return Friend.objects.requests(user=info.context.user)

    @login_required
    def resolve_NumberOfFriendRequests(self, info):
        return Friend.objects.unrejected_request_count(user=info.context.user)

    @login_required
    def resolve_Requestsent(self, info, other_user_id):
        return FriendshipRequest.objects.filter(
            from_user_id=info.context.user.id, to_user_id=other_user_id
        ).exists()
