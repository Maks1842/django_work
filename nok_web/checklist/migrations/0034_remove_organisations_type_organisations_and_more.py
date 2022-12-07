# Generated by Django 4.0.5 on 2022-12-07 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0033_answers_unique_answers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisations',
            name='type_organisations',
        ),
        migrations.AddConstraint(
            model_name='organisations',
            constraint=models.UniqueConstraint(fields=('organisation_name',), name='unique_organisations'),
        ),
    ]
