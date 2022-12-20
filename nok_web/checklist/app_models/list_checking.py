import datetime

from django.contrib.auth.models import User
from django.db import models


'''
Хранятся данные об организациях включенных в конкретную проверку.
А также данные об экспертах, за которыми закрепленны проверяемые организации.
'''
class List_Checking(models.Model):
    checking = models.ForeignKey('Checking', on_delete=models.PROTECT, null=True, verbose_name='Наименование проверки')
    organisation = models.ForeignKey('Organisations', on_delete=models.PROTECT, null=True, verbose_name='Учреждение')
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Эксперт')
    date_check_org = models.DateField(default=datetime.date.today, verbose_name='Дата проверки организации')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    class Meta:
        verbose_name = 'Проверяемая организация'
        verbose_name_plural = 'Проверяемые организации'
