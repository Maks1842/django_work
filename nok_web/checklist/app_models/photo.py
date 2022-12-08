from django.contrib.auth.models import User
from django.db import models


class Photo(models.Model):
    file_name = models.CharField(max_length=50, verbose_name='Фото')
    original_file_name = models.CharField(max_length=50, verbose_name='Оригинальное имя файла')
    description = models.CharField(max_length=50, null=True, blank=True, verbose_name='Комментарий')
    created_at = models.DateField(verbose_name='Дата документа')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')
    user = models.ForeignKey(User, null=True, verbose_name='Пользователь', on_delete=models.PROTECT)

    def __str__(self):
        return self.file_name

    class Meta:
        verbose_name_plural = 'Фото'
