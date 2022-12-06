from django.db import models


class Versions(models.Model):
    table_name = models.CharField(max_length=50, verbose_name='Таблица')
    version = models.CharField(max_length=50, verbose_name='Версия')
    active = models.BooleanField(default=True, verbose_name='Текущая версия')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def __str__(self):
        return self.table_name

    class Meta:
        verbose_name_plural = 'Контроль версий'
