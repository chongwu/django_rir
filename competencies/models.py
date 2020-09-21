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

    class Meta:
        ordering = ('name',)
