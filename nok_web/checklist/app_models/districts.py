from django.db import models

'''
Хранятся наименования районов региона.
'''


class Districts(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    code = models.IntegerField(null=True, blank=True, verbose_name='Код ОКАТО')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Административно-территориальное деление'
        verbose_name_plural = 'Административно-территориальное деление'
