# Generated by Django 4.0.5 on 2022-12-20 13:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0039_remove_profile_profile_remove_profile_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='list_checking',
            name='date_check_org',
            field=models.DateField(default=datetime.date.today, verbose_name='Дата проверки организации'),
        ),
        migrations.AlterField(
            model_name='checking',
            name='date_checking',
            field=models.DateField(verbose_name='Дата начала проверки'),
        ),
    ]