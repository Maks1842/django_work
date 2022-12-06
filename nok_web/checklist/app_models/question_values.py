from django.db import models


class Question_Values(models.Model):
    value_name = models.CharField(max_length=500, verbose_name='Варианты ответов')
    name_alternativ = models.CharField(max_length=100, null=True, blank=True, verbose_name='Альтернативный вариант ответа')

    def __str__(self):
        return self.value_name

    class Meta:

        verbose_name_plural = 'Варианты ответов'
