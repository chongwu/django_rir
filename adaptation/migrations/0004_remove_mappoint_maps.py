# Generated by Django 3.1.6 on 2021-02-17 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adaptation', '0003_auto_20210217_1559'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mappoint',
            name='maps',
        ),
    ]