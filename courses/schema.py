import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from .models import *


class SubLevelType(DjangoObjectType):
    class Meta:
        model = SubLevel
        exclude = ("level",)

    @login_required
    def resolve_content(self, info):
        qs = Progress.objects.filter(course_id=self.id, user=info.context.user)
        if len(qs) > 0:
            return self.content
        raise Exception("U can Not view content without enrolling in course")


class LevelType(DjangoObjectType):
    class Meta:
        model = Level
        exclude = ("course",)


class CourseType(DjangoObjectType):
    class Meta:
        model = Course

    user_enrolled = graphene.Boolean()

    def resolve_user_enrolled(self, info):
        if info.context.user.is_authenticated:
            qs = Progress.objects.filter(course_id=self.id, user=info.context.user)
            if len(qs) > 0:
                return True
        return False


class Query(graphene.ObjectType):
    courses = graphene.List(CourseType)
    course_by_id = graphene.Field(type=CourseType, id=graphene.Int())
    level_by_id = graphene.Field(type=LevelType, id=graphene.Int())
    sublevel_by_id = graphene.Field(type=SubLevelType, id=graphene.Int())

    def resolve_courses(self, info):
        return Course.objects.all().prefetch_related()

    def resolve_course_by_id(self, info, id):
        return Course.objects.prefetch_related().get(id=id)

    def resolve_level_by_id(self, info, id):
        return Level.objects.prefetch_related().get(id=id)

    def resolve_sublevel_by_id(self, info, id):
        return SubLevel.objects.prefetch_related().get(id=id)


class EnrollINCourse(graphene.Mutation):
    created = graphene.Boolean()

    class Arguments:
        course_id = graphene.Int()

    @login_required
    def mutate(self, info, course_id, *args, **kwargs):
        progress, created = Progress.objects.get_or_create(
            course_id=course_id, user=info.context.user
        )
        return EnrollINCourse(created)


class Mutation(graphene.ObjectType):
    enroll_in_course = EnrollINCourse.Field()
