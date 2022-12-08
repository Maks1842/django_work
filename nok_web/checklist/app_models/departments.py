from django.contrib.auth.models import User
from django.db import models

'''
Хранятся наименования департаментов (Министерство культуры Ставропольского края и т.п.).
'''


class Departments(models.Model):
    department_name = models.CharField(max_length=200, verbose_name='Департамент')
    address = models.CharField(max_length=300, null=True, blank=True, verbose_name='Адрес')
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name='Телефон')
    website = models.CharField(max_length=50, null=True, blank=True, verbose_name='Сайт')
    email = models.EmailField(max_length=50, null=True, blank=True, verbose_name='Email')
    parent = models.ForeignKey('Departments', on_delete=models.PROTECT, null=True, blank=True,
                               verbose_name='Parent')  # Поле для отношения к самому себе
    region = models.ForeignKey('Regions', on_delete=models.PROTECT, null=True,
                               verbose_name='Регион')  # Поле для связывания моделей (в данном случае для модели Region)
    type_departments = models.ForeignKey('Type_Departments', on_delete=models.PROTECT, null=True,
                                         verbose_name='Тип департамента')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.PROTECT)

    def __str__(self):
        return self.department_name

    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'
