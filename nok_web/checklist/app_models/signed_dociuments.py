from django.contrib.auth.models import User
from django.db import models

'''
Хранятся ссылки на отсканированные Акты проверки, с подписями представителей проверяемой организации.
'''


class Signed_Dociuments(models.Model):
    file_name = models.CharField(max_length=100, verbose_name='Наименования документов')
    originat_file_name = models.FileField(verbose_name='Ссылка на документ')
    description = models.CharField(max_length=250, verbose_name='Комментарий')
    created_at = models.DateField(verbose_name='Дата документа')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Подписанные Акты'

    def __str__(self):
        return self.file_name
