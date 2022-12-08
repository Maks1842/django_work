from django.contrib.auth.models import User
from django.db import models

'''
В данной модели хранятся все изменения, произведенные пользователем в других моделях.
'''


class Transaction_Exchange(models.Model):
    model = models.CharField(max_length=50, verbose_name='Модель')
    field = models.CharField(max_length=50, verbose_name='Поле')
    old_data = models.CharField(max_length=2000, blank=True, verbose_name='Старые данные')
    new_data = models.CharField(max_length=2000, blank=True, verbose_name='Новые данные')
    date_exchange = models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения данных')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Регистрация изменений данных'
