# Generated by Django 3.1.6 on 2021-02-24 10:47

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0013_auto_20210212_0055'),
        ('adaptation', '0007_auto_20210217_1712'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extrainfo',
            name='map_point_value',
        ),
        migrations.RemoveField(
            model_name='mappointvalue',
            name='value',
        ),
        migrations.AddField(
            model_name='extrainfo',
            name='map_point',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='extra_files', to='adaptation.mappoint', verbose_name='Пункт карты адаптации'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mappoint',
            name='period_of_execution',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Срок исполнения'),
        ),
        migrations.AddField(
            model_name='mappoint',
            name='section',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Раздел (темы)'),
        ),
        migrations.AddField(
            model_name='mappointvalue',
            name='date_of_complete',
            field=models.DateField(blank=True, null=True, verbose_name='Дата выполнения'),
        ),
        migrations.AddField(
            model_name='mappointvalue',
            name='rating',
            field=models.PositiveIntegerField(blank=True, choices=[(0, 'Не выполнено'), (1, 'Частично выполнено'), (2, 'Выполнено')], null=True, verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='conclusion',
            name='final_value',
            field=models.IntegerField(choices=[(1, 'ИС успешно завершен'), (2, 'Продлить АП'), (3, 'ИС не пройден'), (4, 'Рекомендовать досрочно завершить ИС')], verbose_name='Заключение'),
        ),
        migrations.AlterField(
            model_name='mappoint',
            name='form_of_employment',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Офисная'), (2, 'Гибридная'), (3, 'Удаленная')], default=[1, 2, 3], max_length=5, verbose_name='Форма занятости'),
        ),
        migrations.AlterField(
            model_name='mappoint',
            name='positions',
            field=models.ManyToManyField(blank=True, related_name='map_points', to='staff.Position', verbose_name='Должность'),
        ),
    ]
