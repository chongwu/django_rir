from django.contrib import admin
from .models import Position, Staff, Person, Department

# Register your models here.
admin.site.register(Position)
admin.site.register(Person)
admin.site.register(Department)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('person', 'position', 'department')
    list_filter = ('position', 'department')
    search_fields = ('person__fio',)
