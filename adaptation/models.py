from django.db import models
from dateutil.relativedelta import relativedelta
from staff.models import Person, Position

STATUSES = [
    (1, 'В работе'),
    (2, 'На проверке'),
    (3, 'Завершена'),
]

CONCLUSION_TYPES = [
    (1, 'Итоговое'),
    (2, 'HR'),
    (3, 'Руководитель'),
    (4, 'Наставник'),
]

CONCLUSION_VALUES = [
    (1, 'ИС успешно завершен'),
    (2, 'Продлить АП'),
    (3, 'ИС не пройден'),
    (4, 'Рекомендовать досрочно завершить ИС'),
]

MAP_POINT_TYPES = [
    (1, 'Руководитель'),
    (2, 'Рядовой сотрудник')
]

EXTRA_INFO_TYPES = [
    (1, 'Файл'),
    (2, 'Ссылка'),
]


class Map(models.Model):
    employee = models.OneToOneField(Person, on_delete=models.CASCADE, related_name='map',
                                    verbose_name='Сотрудник')
    note = models.TextField(verbose_name='Примечание и комментарии', blank=True, null=True)
    extra_fields = models.JSONField(blank=True, null=True, verbose_name='Дополнительные поля')

    def get_map_end_date(self):
        return self.employee.person_staff.get().date_start + relativedelta(months=3)
    get_map_end_date.short_description = 'Дата окончания ИС'

    class Meta:
        ordering = ('employee__person_staff__date_start',)
        verbose_name = 'Карта адаптации'
        verbose_name_plural = 'Карты адаптаций'


class Conclusion(models.Model):
    type = models.IntegerField(choices=CONCLUSION_TYPES, verbose_name='Тип заключения')
    comment = models.TextField(verbose_name='Комментарий')
    final_value = models.IntegerField(choices=CONCLUSION_VALUES, default=1, verbose_name='Заключение')
    author = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='Автор заключения',
                               related_name='conclusions')
    adaptation_map = models.ForeignKey(Map, on_delete=models.CASCADE, verbose_name='Карта адаптации',
                                       related_name='conclusions')

    class Meta:
        verbose_name = 'Заключение'
        verbose_name_plural = 'Заключения'


class MapPoint(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование пункта')
    positions = models.ManyToManyField(Position, verbose_name='Должность', related_name='map_points')
    point_type = models.IntegerField(choices=MAP_POINT_TYPES, default=1, verbose_name='Тип должности')
    stage_number = models.IntegerField(verbose_name='Номер этапа')
    maps = models.ManyToManyField(Map, through='MapPointValue', verbose_name='Карты адаптаций',
                                  related_name='map_points')

    class Meta:
        verbose_name = 'Пункт карты адаптации'
        verbose_name_plural = 'Пункты карт адаптаций'


class MapPointValue(models.Model):
    map = models.ForeignKey(Map, on_delete=models.CASCADE, verbose_name='Карта адаптации', related_name='point_values')
    map_point = models.ForeignKey(MapPoint, on_delete=models.CASCADE, verbose_name='Карта адаптации',
                                  related_name='point_values')
    value = models.JSONField(verbose_name='Занчение пункта')

    class Meta:
        verbose_name = 'Значение пункта карты адаптации'
        verbose_name_plural = 'Значения пунктов карт адаптаций'


class ExtraInfo(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    type = models.IntegerField(choices=EXTRA_INFO_TYPES, verbose_name='Тип информации')
    path = models.CharField(max_length=255, verbose_name='Путь к информации')
    map_point_value = models.ForeignKey(MapPointValue, on_delete=models.CASCADE, verbose_name='Пункт',
                                        related_name='extra_files')

    class Meta:
        verbose_name = 'Дополнительная информация'
        verbose_name_plural = 'Дополнительная информация'
