# Generated by Django 4.0.5 on 2023-07-27 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0062_regions_district_geojson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisations',
            name='latitude',
            field=models.FloatField(blank=True, max_length=10, null=True, verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='organisations',
            name='longitude',
            field=models.FloatField(blank=True, max_length=10, null=True, verbose_name='Долгота'),
        ),
        migrations.AlterField(
            model_name='regions',
            name='area_geojson',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Административная граница объект в формате Feature GeoJson'),
        ),
        migrations.AlterField(
            model_name='regions',
            name='district_geojson',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Районы региона в формате GeoJson'),
        ),
    ]
