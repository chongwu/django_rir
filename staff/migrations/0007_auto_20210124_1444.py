# Generated by Django 3.1.5 on 2021-01-24 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0006_auto_20210124_0404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=128, unique=True, verbose_name='Наименование отдела'),
        ),
    ]
