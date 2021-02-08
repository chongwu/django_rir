from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea
from .models import Quiz, Question, Choice

import nested_admin


# Register your models here.
class ChoiceInlineAdmin(nested_admin.NestedTabularInline):
    model = Choice
    extra = 1
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': 150})}
    }


class QuestionInlineAdmin(nested_admin.NestedStackedInline):
    model = Question
    extra = 0
    inlines = [ChoiceInlineAdmin]
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': 150})}
    }


class QuizAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInlineAdmin]
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': 150})},
        models.TextField: {'widget': Textarea(attrs={'cols': 150, 'rows': 10})}
    }


admin.site.register(Quiz, QuizAdmin)
