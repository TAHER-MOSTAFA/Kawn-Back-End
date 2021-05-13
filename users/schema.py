import graphene
from django.shortcuts import get_object_or_404
from graphene_django import DjangoConnectionField, DjangoObjectType
from graphql_jwt.decorators import login_required

from kawen.cache_utils import is_online

from .models import Circle, Member


class MemberType(DjangoObjectType):
    class Meta:
        model = Member
        exclude = ["password"]

    IsOnline = graphene.Boolean()

    def resolve_IsOnline(parent, info):
        return is_online(pk=parent.id)



class CircleType(DjangoObjectType):
    class Meta:
        model = Circle


class CreateMember(graphene.Mutation):
    member = graphene.Field(MemberType)

    class Arguments:
        fullName = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, fullName, email, password, *args, **kwargs):
        user = Member(
            full_name=fullName,
            email=email,
        )
        user.set_password(password)
        user.save()
        return CreateMember(member=user)


class CreateCircle(graphene.Mutation):
    circle = graphene.Field(CircleType)

    class Arguments:
        name = graphene.String()
        description = graphene.String()

    def mutate(
        self,
        info,
        name,
        description,
    ):
        circle = Circle(name=name, description=description)
        circle.save()
        return CreateCircle(circle)


class Query(graphene.ObjectType):
    email_is_taken = graphene.Boolean(email=graphene.String())
    circles = graphene.List(CircleType)
    profile = graphene.Field(MemberType)

    @login_required
    def resolve_profile(self, info):
        return info.context.user

    def resolve_circles(
        self,
        info,
    ):
        return Circle.objects.all()

    def resolve_email_is_taken(self, info, email, **Kwargs):
        try:
            Member.objects.get(email=email)
            return True
        except:
            return False


class Mutation(graphene.ObjectType):
    create_member = CreateMember.Field()
    CreateCircle = CreateCircle.Field()
