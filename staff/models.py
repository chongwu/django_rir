from django.db import models
from django.urls import reverse
from competencies.models import Category
from itertools import groupby
from operator import attrgetter


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=128)


class Position(models.Model):
    name = models.CharField(max_length=45)
    competence_category = models.ManyToManyField(Category, related_name='positions')

    def __str__(self):
        return self.name


class Person(models.Model):
    tab_number = models.IntegerField(primary_key=True)
    fio = models.CharField(max_length=128)
    education = models.CharField(max_length=256)
    experience = models.TextField()
    position = models.ManyToManyField(Position, through='Staff', related_name='persons')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='persons', null=True, blank=True)

    class Meta:
        ordering = ('-fio',)

    def __str__(self):
        return self.fio

    def get_absolute_url(self):
        return reverse('staff:person_detail', args=[self.tab_number])

    def current_position(self):
        return self.position.first()

    def get_questionnaire_info(self):
        questionnaire = self.questionnaires.prefetch_related(
            'rows', 'rows__competence', 'rows__competence__category').first()
        rows = {}
        if questionnaire:
            rows = {k: list(v) for k, v in groupby(questionnaire.rows.all(), attrgetter('competence.category.name'))}
        return questionnaire, rows


class Staff(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    date_start = models.DateField()
    date_stop = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = [['person', 'position']]
        ordering = ('-date_start',)

    def __str__(self):
        return f'{self.person.fio} - {self.position.name}'

