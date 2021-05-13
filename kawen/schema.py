import graphene
import graphql_jwt

import chat.schema
import courses.schema
import friends.schema
import notes.schema
import todo.schema
import users.schema


class Query(
    users.schema.Query,
    todo.schema.Query,
    notes.schema.Query,
    courses.schema.Query,
    chat.schema.Query,
    friends.schema.Query,

):
    pass


class Mutation(
    users.schema.Mutation,
    todo.schema.Mutation,
    notes.schema.Mutation,
    courses.schema.Mutation,
    chat.schema.Mutation,
    friends.schema.Mutation,

):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(
    query=Query, mutation=Mutation, subscription=chat.schema.Subscription
)
