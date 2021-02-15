from django.contrib import admin
from .models import Position, Staff, Person, Department

# Register your models here.
admin.site.register(Position)
# admin.site.register(Person)
admin.site.register(Department)


# @admin.register(Staff)
# class StaffAdmin(admin.ModelAdmin):
#     list_display = ('person', 'position', 'department')
#     list_filter = ('position', 'department')
#     search_fields = ('person__fio',)


class PositionInlineAdmin(admin.TabularInline):
    model = Person.position.through
    extra = 0
    verbose_name = 'Место работы'
    verbose_name_plural = 'Список сотрудников'


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('tab_number', 'fio', 'education', 'experience', 'current_department', 'current_position',
                    'employment_form', 'status')
    fields = ('tab_number', 'fio', 'education', 'experience', 'extra_skill', 'employment_form', 'status')

    inlines = (PositionInlineAdmin,)
