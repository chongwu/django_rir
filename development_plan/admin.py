from django.contrib import admin
from .models import DevelopmentPlan, Activity, PlanActivity


class ActivityTabularInline(admin.TabularInline):
    model = Activity
    extra = 1
    verbose_name = 'активность'
    verbose_name_plural = 'активности'


class PlanActivityTabularInline(admin.TabularInline):
    model = PlanActivity
    extra = 1
    verbose_name = 'планируемая активность'
    verbose_name_plural = 'планируемые активности'


@admin.register(DevelopmentPlan)
class DevelopmentPlanAdmin(admin.ModelAdmin):
    inlines = [ActivityTabularInline, PlanActivityTabularInline]

# Register your models here.
