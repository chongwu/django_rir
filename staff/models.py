from django.db import models
from django.urls import reverse
from competencies.models import Category
from itertools import groupby
from operator import attrgetter
from django.contrib.auth.models import User
from model_clone import CloneMixin

EMPLOYMENT_FORMS = [
    (1, 'Офисная'),
    (2, 'Гибридная'),
    (3, 'Удаленная'),
]

EMPLOYMENT_FORMS_DICT = {
    1: 'Офисная',
    2: 'Гибридная',
    3: 'Удаленная',
}

WORK_STATUSES = [
    (1, 'Испытательный срок'),
    (2, 'Работа')
]

WORK_STATUSES_DICT = {
    1: 'Испытательный срок',
    2: 'Работа'
}


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=128, verbose_name='Наименование отдела', unique=True)

    def get_chief(self):
        chief_person = self.persons.filter(position__chief=True).first()
        return chief_person.person if chief_person else None

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Список отделов'
        ordering = ['name']


class Position(CloneMixin, models.Model):
    name = models.CharField(max_length=45, verbose_name='Наименование должности', unique=True)
    competence_category = models.ManyToManyField(Category, related_name='positions',
                                                 verbose_name='Категория компетенций', blank=True)
    chief = models.BooleanField(verbose_name='Является руководителем', default=False)

    _clone_m2m_fields = ['competence_category']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Список должностей'
        ordering = ['name']


class Person(models.Model):
    tab_number = models.IntegerField(primary_key=True, verbose_name='Табельный номер')
    fio = models.CharField(max_length=128, verbose_name='ФИО')
    education = models.CharField(max_length=256, verbose_name='Образование')
    experience = models.TextField(verbose_name='Опыт сотрудника', blank=True, null=True)
    position = models.ManyToManyField(Position, through='Staff', related_name='persons', verbose_name='Должность')
    department = models.ManyToManyField(Department, through='Staff', related_name='workers', verbose_name='Отдел')
    institution = models.TextField(verbose_name='Учебное заведение', blank=True, null=True)
    extra_skill = models.TextField(verbose_name='Дополнительные навыки', blank=True, null=True)
    employment_form = models.IntegerField(choices=EMPLOYMENT_FORMS, default=1,
                                          verbose_name='Форма занятости')
    status = models.IntegerField(choices=WORK_STATUSES, default=2, verbose_name='Статус работы')
    mentor = models.ForeignKey("Person", on_delete=models.CASCADE, related_name='students', verbose_name='Наставник',
                               blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь',
                                related_name='person')

    class Meta:
        ordering = ('tab_number',)
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.fio

    def get_absolute_url(self):
        return reverse('staff:person_detail', args=[self.tab_number])

    def current_position(self):
        return self.position.filter(staff__date_stop__isnull=True).first()

    current_position.short_description = 'Должность'

    def current_position_started(self):
        person_staff = self.person_staff.filter(date_stop__isnull=True).get()
        return person_staff.date_start

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

    def get_employment_form(self):
        return EMPLOYMENT_FORMS_DICT[self.employment_form]


class Staff(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='persons', null=True, blank=True,
                                   verbose_name='Отдел')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='Сотрудник', related_name='person_staff')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name='Должность')
    date_start = models.DateField(verbose_name='Начало работы')
    date_stop = models.DateField(blank=True, null=True, verbose_name='Окончание работы')

    class Meta:
        unique_together = [['person', 'position']]
        ordering = ('-date_start',)
        verbose_name = 'Штат сотрудников'
        verbose_name_plural = 'Штат сотрудников'

    def __str__(self):
        return f'{self.person.fio} - {self.position.name}'
