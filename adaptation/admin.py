from django.contrib import admin
from .models import Map, MapPoint


# Register your models here.
class MapPointTabularInline(admin.TabularInline):
    model = Map.map_points.through
    extra = 1
    verbose_name = 'Пункт'
    verbose_name_plural = 'Пункты'
    fields = ('value',)


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ('pk', 'employee', 'get_map_end_date')
    fields = ('employee', 'note',)
    inlines = [MapPointTabularInline]
