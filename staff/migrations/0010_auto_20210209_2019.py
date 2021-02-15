# Generated by Django 3.1.6 on 2021-02-09 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0009_person_extra_skill'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='employment_form',
            field=models.IntegerField(choices=[(1, 'Офисная'), (2, 'Гибридная'), (3, 'Удаленная')], default=1, max_length=2, verbose_name='Форма занятости'),
        ),
        migrations.AddField(
            model_name='person',
            name='status',
            field=models.IntegerField(choices=[(1, 'Испытательный срок'), (2, 'Работа')], default=2, max_length=2, verbose_name='Статус работы'),
        ),
        migrations.AddField(
            model_name='position',
            name='chief',
            field=models.BooleanField(default=False, verbose_name='Является руководителем'),
        ),
    ]