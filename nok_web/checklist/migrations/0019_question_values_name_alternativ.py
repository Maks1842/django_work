# Generated by Django 4.0.5 on 2022-11-22 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0018_type_organisations_type_departments'),
    ]

    operations = [
        migrations.AddField(
            model_name='question_values',
            name='name_alternativ',
            field=models.CharField(default=1, max_length=100, verbose_name='Альтернативный вариант ответа'),
            preserve_default=False,
        ),
    ]