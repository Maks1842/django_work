from django.db import models

'''
Хранятся наименования регионов.
'''


class Regions(models.Model):
    region_name = models.CharField(max_length=100,
                                   verbose_name='Регион')  # verbose_name - Как поле будет отображаться в админке
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def __str__(self):
        return self.region_name

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'
