# Generated by Django 4.0.5 on 2023-07-06 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0060_organisations_latitude_organisations_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='regions',
            name='area_geojson',
            field=models.CharField(max_length=100, null=True, verbose_name='Административная граница объект в формате Feature GeoJson'),
        ),
    ]