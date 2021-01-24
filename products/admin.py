from django.contrib import admin
from .models import Product, Project

# admin.site.register(Product)


# Register your models here.
class PersonInlineAdmin(admin.TabularInline):
    model = Project.persons.through
    extra = 0
    verbose_name = 'Сотрудника'
    verbose_name_plural = "Список сотрудников"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    fields = ('name', 'city', 'description', 'additional_info', 'product')
    list_display = ('name', 'city', 'description', 'additional_info', 'product', 'persons_list')
    inlines = (PersonInlineAdmin,)


# class ProjectInlineAdmin(admin.TabularInline):
#     fields = ('name', 'city', 'description', 'additional_info')
#     model = Project
#     extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'description', 'additional_info')
    # inlines = (ProjectInlineAdmin,)
