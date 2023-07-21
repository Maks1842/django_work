from django.db import models

'''
Хранятся наименования регионов.
'''


class Regions(models.Model):
    region_name = models.CharField(max_length=100,
                                   verbose_name='Регион')  # verbose_name - Как поле будет отображаться в админке
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')
    area_geojson = models.CharField(max_length=100, blank=True, null=True, verbose_name='Административная граница объект в формате Feature GeoJson')
    district_geojson = models.CharField(max_length=100, blank=True, null=True, verbose_name='Районы региона в формате GeoJson')

    def __str__(self):
        return self.region_name

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'
