from django.contrib.auth import get_user_model
from django.db import models

from users.models import Circle

User = get_user_model()


class Course(models.Model):
    title = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE)
    obj_num = models.IntegerField(default=0)

    """
    Overriding save method so that obj_num is updated automatically
    """

    def save(self, *args, **kwargs):
        x = self.level_set.all().annotate(num_sublevel=models.Count("sublevel"))
        num = 0
        for i in x:
            num += i.num_sublevel
        self.obj_num = num
        super(Course, self).save(*args, **kwargs)


class Level(models.Model):
    title = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class SubLevel(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)


class Question(models.Model):
    body = models.TextField()
    sublevel = models.ForeignKey(SubLevel, on_delete=models.CASCADE)


class Choice(models.Model):
    body = models.CharField(max_length=50)
    answer = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class Project(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to="project")


class ProjectSubmit(models.Model):
    link = models.URLField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class FAQ(models.Model):
    question = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to="FAQ")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.OneToOneField(Course, on_delete=models.CASCADE)


class FAQAnswer(models.Model):
    body = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to="FAQ")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(FAQ, on_delete=models.CASCADE)


class ChallengeGroup(models.Model):
    title = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name="challenge_groups")


class Poductivity(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quizzes = models.SmallIntegerField(default=0)
    projects = models.SmallIntegerField(default=0)


class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.SmallIntegerField(default=0)


class Badge(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField()


class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
