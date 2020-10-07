import graphene
from graphene_django import DjangoObjectType
from .models import Member
from django.shortcuts import get_object_or_404


class MemberType(DjangoObjectType):
    class Meta:
        model = Member
        exclude = ["password"]


class CreateMember(graphene.Mutation):
    member = graphene.Field(MemberType)

    class Arguments:
        fullName = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info,fullName,email,password,*args, **kwargs):
        user = Member(
            full_name=fullName,
            email=email,
        )
        user.set_password(password)
        user.save()
        return CreateMember(member=user)


class Query(graphene.ObjectType):
    members = graphene.List(MemberType)
    check_email = graphene.Boolean(email = graphene.String())

    def resolve_check_email(self, info, email, **Kwargs):
        try:
            Member.objects.get(email=email)
            return True
        except:
            return False


    def resolve_members(self, info, **kwargs):
        return Member.objects.all()
class Mutation(graphene.ObjectType):
    create_member = CreateMember.Field()
