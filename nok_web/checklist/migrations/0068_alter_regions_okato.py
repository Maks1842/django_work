# Generated by Django 4.0.5 on 2023-08-08 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0067_alter_organisations_okato'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regions',
            name='okato',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='Район региона'),
        ),
    ]
