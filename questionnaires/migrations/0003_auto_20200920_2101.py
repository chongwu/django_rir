# Generated by Django 3.1.1 on 2020-09-20 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaires', '0002_auto_20200920_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionnairerow',
            name='competence_val',
            field=models.SmallIntegerField(choices=[(0, 'Отсутствует или не актуальна'), (1, 'Слабо выражена'), (2, 'Среднее владение'), (3, 'Владение на проф. уровне')], default=0),
        ),
        migrations.AlterField(
            model_name='questionnairerow',
            name='questionnaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rows', to='questionnaires.questionnaire'),
        ),
        migrations.AlterField(
            model_name='questionnairerowhistory',
            name='competence_val',
            field=models.SmallIntegerField(choices=[(0, 'Отсутствует или не актуальна'), (1, 'Слабо выражена'), (2, 'Среднее владение'), (3, 'Владение на проф. уровне')], default=0),
        ),
    ]
