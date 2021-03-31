from django.db import models
from dateutil.relativedelta import relativedelta
from staff.models import Person, Position
from competencies.models import Competence
from multiselectfield import MultiSelectField
from workalendar.europe import Russia
from django.db.models import Q
from django.urls import reverse

STATUSES = [
    (1, 'В работе'),
    (2, 'На проверке'),
    (3, 'Завершена'),
]

CONCLUSION_TYPES = [
    (1, 'Наставник'),
    (2, 'Руководитель'),
    (3, 'HR'),
    (4, 'Итоговое'),
]

CONCLUSION_VALUES = [
    (1, 'ИС успешно завершен'),
    (2, 'Продлить АП'),
    (3, 'ИС не пройден'),
    (4, 'Рекомендовать досрочно завершить ИС'),
]

MAP_POINT_TYPES = [
    (1, 'Все сотрудники'),
    (2, 'Руководитель'),
    (3, 'Рядовой сотрудник')
]

EXTRA_INFO_TYPES = [
    (1, 'Файл'),
    (2, 'Ссылка'),
]
FORMS_OF_EMAPLOYMENTS = [
    (1, 'Офисная'),
    (2, 'Гибридная'),
    (3, 'Удаленная'),
]
RATING_VALUES = [
    (0, 'Не выполнено'),
    (1, 'Частично выполнено'),
    (2, 'Выполнено'),
]

RATINGS = {
    0: 'Не выполнено',
    1: 'Частично выполнено',
    2: 'Выполнено',
}

CONCLUSIONS = {
    1: 'ИС успешно завершен',
    2: 'Продлить АП',
    3: 'ИС не пройден',
    4: 'Рекомендовать досрочно завершить ИС',
}


class Map(models.Model):
    employee = models.OneToOneField(Person, on_delete=models.CASCADE, related_name='map',
                                    verbose_name='Сотрудник')
    note = models.TextField(verbose_name='Примечание и комментарии', blank=True, null=True)
    extra_fields = models.JSONField(blank=True, null=True, verbose_name='Дополнительные поля')

    def get_absolute_url(self):
        return reverse('adaptation:map_detail', args=[str(self.id)])

    def get_map_end_date(self):
        return self.employee.person_staff.get().date_start + relativedelta(months=3)

    get_map_end_date.short_description = 'Дата окончания ИС'

    def map_result(self):
        first_stage_success = self.map_point_values.filter((Q(map_point__stage_number=1) | Q(stage=1)) & Q(rating=2)).count()
        first_stage_all = self.map_point_values.filter(Q(map_point__stage_number=1) | Q(stage=1)).count()
        other_stage_success = self.map_point_values.filter((Q(map_point__stage_number__gt=1) | Q(stage__gt=1)) & Q(rating=2)).count()
        other_stage_all = self.map_point_values.filter(Q(map_point__stage_number__gt=1) | Q(stage__gt=1)).count()
        return (first_stage_success/first_stage_all) * 0.7 + (other_stage_success/other_stage_all) * 0.3
        # return self.map_point_values.filter(rating=2).count() / self.map_point_values.count()

    map_result.short_description = 'Результат испытательного срока'

    def map_result_float(self):
        return self.map_result() * 100

    def map_result_readable_value(self):
        result = None
        value = self.map_result_float()
        if value < 70:
            result = 'Неудовлетворительный'
        elif 70 <= value < 90:
            result = 'Удовлетворительный'
        elif value >= 90:
            result = 'Успешный'
        return result

    def map_result_percent(self):
        return "{0:.0%}".format(self.map_result())

    class Meta:
        ordering = ('employee__person_staff__date_start',)
        verbose_name = 'Карта адаптации'
        verbose_name_plural = 'Карты адаптаций'


class Conclusion(models.Model):
    type = models.IntegerField(choices=CONCLUSION_TYPES, verbose_name='Тип заключения')
    comment = models.TextField(verbose_name='Комментарий')
    final_value = models.IntegerField(choices=CONCLUSION_VALUES, verbose_name='Заключение')
    author = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='Автор заключения',
                               related_name='conclusions')
    adaptation_map = models.ForeignKey(Map, on_delete=models.CASCADE, verbose_name='Карта адаптации',
                                       related_name='conclusions')

    def get_final_value(self):
        return CONCLUSIONS[self.final_value]

    class Meta:
        verbose_name = 'Заключение'
        verbose_name_plural = 'Заключения'


class MapPoint(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование пункта')
    stage_number = models.PositiveIntegerField(verbose_name='Номер этапа')
    form_of_employment = MultiSelectField(choices=FORMS_OF_EMAPLOYMENTS, verbose_name='Форма занятости',
                                          default=[1, 2, 3])
    # @TODO Продумать логику работы с рабочими днями (+ Российские праздники)
    period_of_execution = models.PositiveIntegerField(blank=True, null=True, verbose_name='Срок исполнения',
                                                      help_text='Количество рабочих дней')
    section = models.CharField(max_length=255, blank=True, null=True, verbose_name='Раздел (темы)')
    # form_of_employment = models.PositiveIntegerField(choices=FORMS_OF_EMAPLOYMENTS, default=1,
    #                                                  verbose_name='Форма занятости')
    point_type = models.IntegerField(choices=MAP_POINT_TYPES, default=1, verbose_name='Тип должности')
    positions = models.ManyToManyField(Position, verbose_name='Должность', related_name='map_points', blank=True)

    # maps = models.ManyToManyField(Map, through='MapPointValue', verbose_name='Карты адаптаций',
    #                               related_name='map_points')

    def __str__(self):
        return self.name

    def get_positions(self):
        return ', '.join(map(str, self.positions.all()))
    get_positions.short_description = 'Должности'

    def get_period_of_execution(self):
        return f'Не позднее {self.period_of_execution} раб. дн.' if self.period_of_execution else None
    get_period_of_execution.short_description = 'Срок исполнения'

    class Meta:
        verbose_name = 'Пункт карты адаптации'
        verbose_name_plural = 'Пункты карт адаптаций'
        ordering = ('pk',)


class MapPointValue(models.Model):
    map = models.ForeignKey(Map, on_delete=models.CASCADE, verbose_name='Карта адаптации',
                            related_name='map_point_values')
    map_point = models.ForeignKey(MapPoint, on_delete=models.CASCADE, verbose_name='Карта адаптации',
                                  related_name='point_values', null=True)
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE, verbose_name='Компетенция',
                                   related_name='map_point_values', null=True)
    name = models.CharField(max_length=255, verbose_name='Наименование пункта', null=True, blank=True)
    stage = models.PositiveIntegerField(verbose_name='Этап', null=True, blank=True)
    rating = models.PositiveIntegerField(choices=RATING_VALUES, blank=True, null=True, verbose_name='Оценка')
    date_of_complete = models.DateField(null=True, blank=True, verbose_name='Дата выполнения')

    # value = models.JSONField(verbose_name='Занчение пункта')

    def get_name(self):
        return self.map_point.name if self.map_point else self.name

    def get_files(self):
        if self.map_point:
            return ', '.join([extra_file.name for extra_file in self.map_point.extra_files.all()])
        return '-'

    def get_completing_date(self):
        if self.map_point:
            period_of_execution = self.map_point.period_of_execution
            if period_of_execution:
                cal = Russia()
                return cal.add_working_days(self.map.employee.current_position_started(), self.map_point.period_of_execution)
        return '-'
    get_completing_date.short_description = 'Выполнить до:'

    def get_rating(self):
        return RATINGS[self.rating] if self.rating else ''

    def get_all_ratings(self):
        return RATING_VALUES

    class Meta:
        verbose_name = 'Значение пункта карты адаптации'
        verbose_name_plural = 'Значения пунктов карт адаптаций'


class ExtraInfo(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    type = models.IntegerField(choices=EXTRA_INFO_TYPES, verbose_name='Тип информации')
    link = models.CharField(max_length=255, verbose_name='Ссылка', blank=True, null=True)
    extra_info_file = models.FileField(blank=True, null=True, upload_to='extra_info', verbose_name='Файл')
    # path = models.CharField(max_length=255, verbose_name='Путь к информации')
    map_point = models.ForeignKey(MapPoint, on_delete=models.CASCADE, verbose_name='Пункт карты адаптации',
                                  related_name='extra_files')

    class Meta:
        verbose_name = 'Дополнительная информация'
        verbose_name_plural = 'Дополнительная информация'
