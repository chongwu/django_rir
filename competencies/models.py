from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=45, verbose_name='Имя')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Competence(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='competencies', verbose_name='Категория')
    level_0 = models.TextField(verbose_name='Уровень 0', blank=True, null=True)
    level_1 = models.TextField(verbose_name='Уровень 1', blank=True, null=True)
    level_2 = models.TextField(verbose_name='Уровень 2', blank=True, null=True)
    level_3 = models.TextField(verbose_name='Уровень 3', blank=True, null=True)

    def __str__(self):
        return self.name

    @classmethod
    def prepare_report(cls, data):
        rows = {}
        for row in data.all():
            if row['competence__category__name'] not in rows:
                rows[row['competence__category__name']] = [row]
            else:
                rows[row['competence__category__name']].append(row)
        return rows

    class Meta:
        ordering = ('name',)
        verbose_name = 'Компетенция'
        verbose_name_plural = 'Компетенции'
