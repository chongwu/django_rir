from django.db import models
from staff.models import Person
from competencies.models import Competence

VAL_CHOICES = (
        (0, 'Отсутствует или не актуальна'),
        (1, 'Слабо выражена'),
        (2, 'Среднее владение'),
        (3, 'Владение на проф. уровне'),
    )


# Create your models here.
class Questionnaire(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='questionnaires',
                               verbose_name='Сотрудник')
    date = models.DateField(auto_now_add=True, verbose_name='Дата прохождения')
    competencies = models.ManyToManyField(Competence, through='QuestionnaireRow', related_name='questionnaires',
                                          verbose_name='Компетенции')

    def get_competencies(self):
        return ', '.join([competence.name for competence in self.competencies.all()])
    get_competencies.short_description = 'Компетенции'

    def __str__(self):
        return f'Анкета сотрудника: {self.person.fio}'

    class Meta:
        ordering = ('-date',)
        verbose_name = 'Анкета'
        verbose_name_plural = 'Анкеты'


class QuestionnaireRow(models.Model):

    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name='rows')
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)
    competence_val = models.SmallIntegerField(default=0, choices=VAL_CHOICES)
    date = models.DateField(auto_now=True, blank=True, null=True)

    def get_human_read_value(self):
        return VAL_CHOICES[self.competence_val][1]


class QuestionnaireRowHistory(models.Model):
    questionnaire_row = models.ForeignKey(QuestionnaireRow, on_delete=models.CASCADE, related_name='history')
    competence_val = models.SmallIntegerField(default=0, choices=VAL_CHOICES)
    date = models.DateField()
