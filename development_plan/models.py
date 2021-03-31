from django.core.validators import MinValueValidator
from django.db import models

from staff.models import Person

ACTIVITY_TYPES = [
    (1, 'Электронное обучение')
]

STATUSES = [
    (0, 'Не утверждено'),
    (1, 'На рассмотрении'),
    (2, 'Утверждено'),
]

ACTIVITY_STATUSES = [
    (0, 'Не выполненные'),
    (1, 'Запланированные'),
    (2, 'Выполненные'),
]

ACTIVITY_STATUSES_DICT = {
    0: 'Не выполненные',
    1: 'Запланированные',
    2: 'Выполненные',
}

ACTIVITY_TYPES_DICT = {
    1: 'Электронное обучение'
}


# Create your models here.
class DevelopmentPlan(models.Model):
    employee = models.OneToOneField(Person, on_delete=models.CASCADE, related_name='dev_plan',
                                    verbose_name='Сотрудник')

    def __str__(self):
        return self.employee.fio

    class Meta:
        verbose_name = 'Индивидуальный план развития'
        verbose_name_plural = 'Индивидуальные планы развития'


class Activity(models.Model):
    plan = models.ForeignKey(DevelopmentPlan, on_delete=models.CASCADE, related_name='activities')
    values = models.CharField(max_length=255, verbose_name='Развитие ПТЗН/Ценности', blank=True, null=True)
    activity_status = models.PositiveIntegerField(choices=ACTIVITY_STATUSES,
                                                  verbose_name='Статус активности')
    activity_type = models.PositiveIntegerField(choices=ACTIVITY_TYPES, verbose_name='Тип активности')
    name = models.CharField(max_length=255, verbose_name='Наименование')
    hours = models.FloatField(validators=[MinValueValidator(0.1)], verbose_name='Объем',
                              help_text='Кол-во академических часов')
    required_up_to = models.DateField(blank=True, null=True, verbose_name='Требуется до')
    status = models.PositiveIntegerField(blank=True, null=True, choices=STATUSES, verbose_name='Статус')
    start = models.DateField(blank=True, null=True, verbose_name='Начато (запланировано)')
    stop = models.DateField(blank=True, null=True, verbose_name='Завершено')
    note = models.CharField(max_length=255, blank=True, null=True, verbose_name='Причина не выполнениня')

    def get_status(self):
        return ACTIVITY_STATUSES_DICT[self.status]

    def get_type(self):
        return ACTIVITY_TYPES_DICT[self.activity_type]


class PlanActivity(models.Model):
    plan = models.ForeignKey(DevelopmentPlan, on_delete=models.CASCADE, related_name='plan_activities')
    values = models.CharField(max_length=255, verbose_name='Развитие ПТЗН/Ценности')
    method = models.CharField(max_length=255, verbose_name='Метод развития')
    required_up_to = models.DateField(verbose_name='Требуется до')
    activity = models.CharField(max_length=255, verbose_name='Планируемая активность')
