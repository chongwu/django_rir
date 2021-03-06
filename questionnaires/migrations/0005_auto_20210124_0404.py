# Generated by Django 3.1.5 on 2021-01-24 01:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('competencies', '0003_auto_20210124_0404'),
        ('staff', '0006_auto_20210124_0404'),
        ('questionnaires', '0004_auto_20200920_2104'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questionnaire',
            options={'ordering': ('-date',), 'verbose_name': 'Анкета', 'verbose_name_plural': 'Анкеты'},
        ),
        migrations.AlterField(
            model_name='questionnaire',
            name='competencies',
            field=models.ManyToManyField(related_name='questionnaires', through='questionnaires.QuestionnaireRow', to='competencies.Competence', verbose_name='Компетенции'),
        ),
        migrations.AlterField(
            model_name='questionnaire',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='Дата прохождения'),
        ),
        migrations.AlterField(
            model_name='questionnaire',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionnaires', to='staff.person', verbose_name='Сотрудник'),
        ),
    ]
