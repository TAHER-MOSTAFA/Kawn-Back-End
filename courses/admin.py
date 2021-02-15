import nested_admin
from django.contrib import admin

from .models import *


class StackedChoice(nested_admin.NestedStackedInline):
    model = Choice
    extra = 4


class StackedQustion(nested_admin.NestedStackedInline):
    model = Question
    inlines = (StackedChoice,)
    extra = 0


class StackedSubLevel(nested_admin.NestedStackedInline):
    model = SubLevel
    inlines = (StackedQustion,)
    extra = 0


class StackedLevel(nested_admin.NestedStackedInline):
    model = Level
    inlines = (StackedSubLevel,)
    extra = 0


@admin.register(Course)
class LevelAdmin(nested_admin.NestedModelAdmin):
    inlines = (StackedLevel,)
