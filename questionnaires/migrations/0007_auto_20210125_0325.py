# Generated by Django 3.1.5 on 2021-01-25 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaires', '0006_auto_20210125_0314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionnairerowhistory',
            name='competence_val',
            field=models.SmallIntegerField(choices=[(0, 'Отсутствует или не актуальна'), (1, 'Слабо выражена'), (2, 'Среднее владение'), (3, 'Владение на проф. уровне')]),
        ),
        migrations.AlterField(
            model_name='questionnairerowhistory',
            name='new_competence_val',
            field=models.SmallIntegerField(choices=[(0, 'Отсутствует или не актуальна'), (1, 'Слабо выражена'), (2, 'Среднее владение'), (3, 'Владение на проф. уровне')]),
        ),
    ]
