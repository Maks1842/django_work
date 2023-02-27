from django.db import models


class Question_Values(models.Model):
    value_name = models.CharField(max_length=500, verbose_name='Варианты ответов')
    name_alternativ = models.CharField(max_length=100, blank=True, verbose_name='Второй вариант ответа')
    special_option = models.BooleanField(default=False, verbose_name='Признак альтернативной опции ответа')

    def __str__(self):
        return self.value_name

    class Meta:

        verbose_name_plural = 'Варианты ответов'
