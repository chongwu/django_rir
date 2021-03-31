from django.db import models
from django.contrib import admin
from .models import Map, MapPoint, ExtraInfo
from staff.models import Position
from django.forms import CheckboxSelectMultiple
import json


# Register your models here.
class ExtraInfoTabularInline(admin.StackedInline):
    model = ExtraInfo
    extra = 1
    verbose_name = 'дополнительный материал'
    verbose_name_plural = 'Дополнительные материалы'


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ('pk', 'employee', 'get_map_end_date')
    fields = ('employee', 'note',)


@admin.register(MapPoint)
class MapPointAdmin(admin.ModelAdmin):
    list_display = ('name', 'stage_number', 'point_type', 'get_period_of_execution', 'get_positions')
    list_filter = ('point_type', 'positions', 'stage_number',)
    search_fields = ['name']
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple}
    }
    inlines = [ExtraInfoTabularInline]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if extra_context is None:
            map_point = MapPoint.objects.get(pk=object_id)
            extra_context = {
                'positions': json.dumps(list(map_point.positions.values_list('id', flat=True))),
                'extra_files': json.dumps(list(map_point.extra_files.values_list('id', 'type'))),
            }
        return super().change_view(request, object_id, form_url, extra_context)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if request.POST.get('point_type') == '1':
            positions = Position.objects.all()
            form.instance.positions.add(*positions)
