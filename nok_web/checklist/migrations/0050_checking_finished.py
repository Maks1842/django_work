# Generated by Django 4.0.5 on 2023-02-09 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0049_type_templates_alter_organisations_inn_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='checking',
            name='finished',
            field=models.BooleanField(default=False, verbose_name='Признак завершения проверки'),
        ),
    ]
