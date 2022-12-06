from django.db import models

'''
С помощью какого элемента пользователь проставояет ответ:
1 - checkbox;
2 - radiobutton;
3 - input;
5 - select.
'''


class Type_Answers(models.Model):
    type = models.CharField(max_length=50, verbose_name='Типы ответов')

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Тип ответа'
        verbose_name_plural = 'Типы ответов'
