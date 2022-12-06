from django.db import models


class Comments(models.Model):
    free_value = models.CharField(max_length=500, verbose_name='Комментарии')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    class Meta:
        verbose_name_plural = 'Комментарии'
