# Generated by Django 3.1.1 on 2020-09-12 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='date_stop',
            field=models.DateField(blank=True, null=True),
        ),
    ]
