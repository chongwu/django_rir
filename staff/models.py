from django.db import models
from django.urls import reverse
from competencies.models import Category
from itertools import groupby
from operator import attrgetter


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=128, verbose_name='Наименование отдела')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Список отделов'


class Position(models.Model):
    name = models.CharField(max_length=45, verbose_name='Наименование должности')
    competence_category = models.ManyToManyField(Category, related_name='positions',
                                                 verbose_name='Категория компетенций')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Список должностей'


class Person(models.Model):
    tab_number = models.IntegerField(primary_key=True, verbose_name='Табельный номер')
    fio = models.CharField(max_length=128, verbose_name='ФИО')
    education = models.CharField(max_length=256, verbose_name='Образование')
    experience = models.TextField(verbose_name='Опыт сотрудника')
    position = models.ManyToManyField(Position, through='Staff', related_name='persons', verbose_name='Должность')
    department = models.ManyToManyField(Department, through='Staff', related_name='workers', verbose_name='Отдел')

    class Meta:
        ordering = ('-fio',)
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.fio

    def get_absolute_url(self):
        return reverse('staff:person_detail', args=[self.tab_number])

    def current_position(self):
        return self.position.first()
    current_position.short_description = 'Должность'

    def current_department(self):
        return self.department.first()
    current_department.short_description = 'Отдел'

    def get_questionnaire_info(self):
        questionnaire = self.questionnaires.prefetch_related(
            'rows', 'rows__competence', 'rows__competence__category').first()
        rows = {}
        if questionnaire:
            rows = {k: list(v) for k, v in groupby(questionnaire.rows.all(), attrgetter('competence.category.name'))}
        return questionnaire, rows


class Staff(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='Сотрудник')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name='Должность')
    date_start = models.DateField(verbose_name='Начало работы')
    date_stop = models.DateField(blank=True, null=True, verbose_name='Окончание работы')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='persons', null=True, blank=True,
                                   verbose_name='Отдел')

    class Meta:
        unique_together = [['person', 'position']]
        ordering = ('-date_start',)
        verbose_name = 'Штат сотрудников'
        verbose_name_plural = 'Штат сотрудников'

    def __str__(self):
        return f'{self.person.fio} - {self.position.name}'

