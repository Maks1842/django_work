from django.db import models

'''
Хранятся наименования районов региона.
'''


class Districts(models.Model):
    name = models.CharField(max_length=100,
                                   verbose_name='Район региона')
    code = models.IntegerField(null=True, blank=True, verbose_name='Код района')
    region = models.ForeignKey('Regions', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Регион')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Районы регионов'
        verbose_name_plural = 'Районы регионов'
