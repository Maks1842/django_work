# Generated by Django 4.0.5 on 2023-01-16 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0041_list_checking_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='form_sections_question',
            name='required',
            field=models.BooleanField(default=True, verbose_name='Признак обязательности'),
        ),
    ]
