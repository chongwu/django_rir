from django.db import models


# Create your models here.
class Quiz(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание теста')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Question(models.Model):
    text = models.CharField(max_length=255, verbose_name='Текст вопроса')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Choice(models.Model):
    text = models.CharField(max_length=255, verbose_name='Текст ответа')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    correct = models.BooleanField(default=False, verbose_name='Верный ответ')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
