import graphene 
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from django.contrib.auth import get_user_model
from .models import *

member = get_user_model()

class TaskType(DjangoObjectType):
    class Meta:
        model = Task


class TaskCardType(DjangoObjectType):
    class Meta:
        model = TaskCard
    

class CreateTaskCard(graphene.Mutation):
    taskcard = graphene.Field(TaskCardType)

    class Arguments:
        name = graphene.String(required=True)
    
    @login_required
    def mutate(self, info, name, *args, **kwargs):
        card = TaskCard.objects.create(name=name,user=info.context.user)
        return CreateTaskCard(taskcard=card)


class CreateTask(graphene.Mutation):
    task = graphene.Field(TaskType)

    class Arguments:
        name = graphene.String(required=True)
        deadline = graphene.DateTime(required=False)
        taskcard = graphene.Int(required=True)
    
    @login_required
    def mutate(self, info, name, taskcard, deadline=None,*args, **kwargs):
        try : 
            card = TaskCard.objects.get(user=info.context.user, id=taskcard)
        except:
            raise Exception("No Such Task Card")
        card.num += 1
        task = Task.objects.create(name=name,taskcard=card,deadline=deadline)
        return CreateTask(task)


class UpdateTask(graphene.Mutation):
    task = graphene.Field(TaskType)

    class Arguments:
        id = graphene.Int(required=True)
        card_id = graphene.Int(required=True)
        name = graphene.String(required=False)
        deadline = graphene.DateTime(required=False)
        done = graphene.Boolean(required=False)
    
    @login_required
    def mutate(self, info, id, card_id, *args, **kwargs):
        try : 
            taskcard = TaskCard.objects.get(user=info.context.user, id=card_id)
        except:
            raise Exception("No Such Task Card")
        task = Task.objects.filter(id=id)
        task.update(**kwargs)
        return UpdateTask(task[0]) 

class DeleteTask(graphene.Mutation):
    message = graphene.String()
    class Arguments:
        id = graphene.Int(required=True)
        card_id = graphene.Int(required=True)


    @login_required
    def mutate(self, info, id, card_id, *args, **kwargs):
        try : 
            taskcard = TaskCard.objects.get(user=info.context.user, id=card_id)
        except:
            raise Exception("No Such Task Card")
        taskcard.num -= 1
        task = Task.objects.filter(id=id).delete()
        return DeleteTask("Done")


class UpdateTaskCard(graphene.Mutation):
    taskcard = graphene.Field(TaskCardType)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
    @login_required
    def mutate(self, info,id ,name, *args, **kwargs):
        try : 
            taskcard = TaskCard.objects.get(user=info.context.user, id=id)
        except:
            raise Exception("No Such Task Card")
        taskcard.name = name
        return UpdateTaskCard(taskcard=taskcard)



class DeleteTaskCard(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    @login_required
    def mutate(self, info, id , *args, **kwargs):
        try : 
            taskcard = TaskCard.objects.get(user=info.context.user, id=id).delete()
        except:
            raise Exception("No Such Task Card")
        return DeleteTaskCard("Done")



class Query(graphene.ObjectType):
    todo = graphene.List(TaskCardType)
    
    @login_required
    def resolve_todo(self,info):
        return TaskCard.objects.filter(user=info.context.user).prefetch_related('task')


class Mutation(graphene.ObjectType):
    Create_Task = CreateTask.Field()
    Update_Task = UpdateTask.Field()
    Delete_Task = DeleteTask.Field()
    Create_TaskCard = CreateTaskCard.Field()
    Update_TaskCard = UpdateTaskCard.Field()
    Delete_TaskCard = DeleteTaskCard.Field()
