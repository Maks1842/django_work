from django.db import models

'''
Хранятся данные о должностях компании НОК.
'''

class Profile_Position(models.Model):
    position = models.CharField(max_length=100, verbose_name='Должность')

    class Meta:
        verbose_name_plural = 'Должности'