from graphql_jwt.signals import token_issued, token_refreshed
from graphene import Mutation
from django.contrib.auth.signals import user_logged_in



def userloggedin(user,request,sender, *args, **kwargs):
    user_logged_in.send(sender=sender,request=request, user=user)

token_issued.connect(userloggedin)
token_refreshed.connect(userloggedin)