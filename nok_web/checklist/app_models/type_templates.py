from django.db import models

'''
Типы шаблонов хранящиеся в templates:
1 - Акт;
2 - Рейтинг;
'''


class Type_Templates(models.Model):
    type = models.CharField(max_length=20, verbose_name='Тип шаблона')

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Тип шаблона'
        verbose_name_plural = 'Типы шаблонов'