# Generated by Django 4.0.5 on 2023-08-28 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0070_organisation_persons_use_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='districts',
            name='code',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='Код ОКАТО'),
        ),
    ]
