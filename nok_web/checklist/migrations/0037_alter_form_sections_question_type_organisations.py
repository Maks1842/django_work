# Generated by Django 4.0.5 on 2022-12-12 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0036_alter_department_persons_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form_sections_question',
            name='type_organisations',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='id Типов учреждений'),
        ),
    ]
