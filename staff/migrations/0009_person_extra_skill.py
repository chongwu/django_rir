# Generated by Django 3.1.5 on 2021-01-24 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0008_auto_20210124_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='extra_skill',
            field=models.TextField(blank=True, null=True, verbose_name='Дополнительные навыки'),
        ),
    ]