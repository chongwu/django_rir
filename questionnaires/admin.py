from django.contrib import admin
from .models import Questionnaire, QuestionnaireRow, QuestionnaireRowHistory

# Register your models here.
admin.site.register(QuestionnaireRow)
admin.site.register(QuestionnaireRowHistory)


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('person', 'date')
    list_filter = ('date',)
    search_fields = ('person__fio',)

