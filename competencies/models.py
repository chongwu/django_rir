from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Competence(models.Model):
    name = models.CharField(max_length=45)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='competencies')

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
