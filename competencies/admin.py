from django.contrib import admin

from .models import Competence, Category
from .views import import_competencies
from django.urls import path, reverse
from django.forms import Textarea
from django.db import models

# Register your models here.
# admin.site.register(Competence)


class CompetenceInlineAdmin(admin.TabularInline):
    model = Competence
    extra = 1

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 5, 'cols': 30})}
    }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/model_change_list.html'
    inlines = (CompetenceInlineAdmin,)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import_competencies/', import_competencies, name='import_competencies'),
        ]
        return my_urls + urls
