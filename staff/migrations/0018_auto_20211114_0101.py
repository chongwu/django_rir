# Generated by Django 3.1.6 on 2021-11-13 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competencies', '0006_auto_20211114_0101'),
        ('staff', '0017_auto_20210523_1254'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'ordering': ['name'], 'verbose_name': 'Отдел', 'verbose_name_plural': 'Список отделов'},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ('tab_number',), 'verbose_name': 'Сотрудник', 'verbose_name_plural': 'Сотрудники'},
        ),
        migrations.AlterModelOptions(
            name='position',
            options={'ordering': ['name'], 'verbose_name': 'Должность', 'verbose_name_plural': 'Список должностей'},
        ),
        migrations.AlterField(
            model_name='position',
            name='competence_category',
            field=models.ManyToManyField(blank=True, related_name='positions', to='competencies.Category', verbose_name='Категория компетенций'),
        ),
    ]
