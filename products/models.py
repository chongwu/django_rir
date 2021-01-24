from django.db import models


# Create your models here.
from staff.models import Person


class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name='Наименование продукта')
    region = models.CharField(max_length=50, verbose_name='Регион', blank=True, null=True)
    description = models.TextField(verbose_name='Описание продукта')
    additional_info = models.TextField(verbose_name='Дополнительная информация', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Project(models.Model):
    name = models.CharField(max_length=256, verbose_name='Наименование проекта')
    city = models.CharField(max_length=25, verbose_name='Город', blank=True, null=True)
    description = models.TextField(verbose_name='Описание проекта')
    additional_info = models.TextField(verbose_name='Дополнительная информация', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='projects', verbose_name='Продукт')
    persons = models.ManyToManyField(Person, related_name='projects', verbose_name='Сотрудники')

    def persons_list(self):
        return ', '.join(person.fio for person in self.persons.all())
    persons_list.short_description = 'Список сотрудников'

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
