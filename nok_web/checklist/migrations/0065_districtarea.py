# Generated by Django 4.0.5 on 2023-08-07 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0064_regions_code_districts_organisations_district'),
    ]

    operations = [
        migrations.CreateModel(
            name='DistrictArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField(null=True, verbose_name='Результаты')),
            ],
        ),
    ]
