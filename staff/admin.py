from django.contrib import admin
from .models import Position, Staff, Person, Department
from .views import upload_persons_list
from django.urls import path

# Register your models here.
# admin.site.register(Position)
# admin.site.register(Person)
admin.site.register(Department)


# @admin.register(Staff)
# class StaffAdmin(admin.ModelAdmin):
#     list_display = ('person', 'position', 'department')
#     list_filter = ('position', 'department')
#     search_fields = ('person__fio',)
def clone_model(modeladmin, request, queryset):
    for position in queryset:
        position.make_clone()
clone_model.short_description = "Создать копию должности/должностей"


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    actions = [clone_model]


class PositionInlineAdmin(admin.TabularInline):
    model = Person.position.through
    extra = 0
    verbose_name = 'Место работы'
    verbose_name_plural = 'Список сотрудников'


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    change_list_template = 'admin/model_change_list.html'
    list_display = ('tab_number', 'fio', 'education', 'experience', 'current_department', 'current_position',
                    'employment_form', 'status')
    search_fields = ('fio',)
    fields = (
    'tab_number', 'fio', 'user', 'education', 'institution', 'experience', 'extra_skill', 'employment_form', 'status',
    'mentor')
    list_filter = ('education', 'employment_form', 'status')

    inlines = (PositionInlineAdmin,)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import_persons/', upload_persons_list, name='import_persons'),
        ]
        return my_urls + urls
