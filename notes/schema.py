from .models import Note
import graphene 
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

class NoteType(DjangoObjectType):
    class Meta:
        model = Note

class CreateNote(graphene.Mutation):
    note = graphene.Field(NoteType)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)

    @login_required
    def mutate(self, info, name, description, *args, **kwargs):
        n = Note.objects.create(name=name, description=description, user=info.context.user)
        return CreateNote(n)


class UpdateNote(graphene.Mutation):
    note = graphene.Field(NoteType)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        description = graphene.String()

    @login_required
    def mutate(self, info, id, *args, **kwargs):
        try:
            n = Note.objects.filter(user=info.context.user, id=id)
        except:
            raise Exception("No such Note")
        n.update(**kwargs)
        return CreateNote(n[0])

class DeleteNote(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    @login_required
    def mutate(self, info, id, *args, **kwargs):
        try:
            n = Note.objects.get(user=info.context.user, id=id).delete()
        except:
            raise Exception("No such Note")
        return DeleteNote("Done")

class Query(graphene.ObjectType):
    Notes = graphene.List(NoteType)

    @login_required
    def resolve_Notes(self,info):
        return Note.objects.filter(user=info.context.user)

class Mutation(graphene.ObjectType):
    Create_Note = CreateNote.Field()
    Delete_Note = DeleteNote.Field()
    Update_Note = UpdateNote.Field()


    

