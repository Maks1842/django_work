# Generated by Django 4.0.5 on 2022-11-22 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0019_question_values_name_alternativ'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question_values',
            name='name_alternativ',
            field=models.CharField(blank=True, max_length=100, verbose_name='Альтернативный вариант ответа'),
        ),
    ]