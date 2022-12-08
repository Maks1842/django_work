from django.db import models

'''
Хранятся данные о проверке.
'''


class Checking(models.Model):
    name = models.CharField(max_length=500, verbose_name='Наименование проверки')
    date_checking = models.DateField(verbose_name='Дата проверки')
    region = models.ForeignKey('Regions', on_delete=models.PROTECT, null=True, verbose_name='Регион')
    department = models.ForeignKey('Departments', on_delete=models.PROTECT, null=True, verbose_name='Департамент')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Наименование проверки'
