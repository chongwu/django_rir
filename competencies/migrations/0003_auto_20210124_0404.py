# Generated by Django 3.1.5 on 2021-01-24 01:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('competencies', '0002_auto_20201011_1655'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',), 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='competence',
            options={'ordering': ('name',), 'verbose_name': 'Компетенция', 'verbose_name_plural': 'Компетенции'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=45, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='competence',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competencies', to='competencies.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='competence',
            name='name',
            field=models.CharField(max_length=45, unique=True, verbose_name='Имя'),
        ),
    ]
