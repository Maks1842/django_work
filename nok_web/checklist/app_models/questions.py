from django.db import models


class Questions(models.Model):
    questions = models.CharField(max_length=2000, verbose_name='Вопросы')

    def __str__(self):
        return self.questions

    class Meta:
        verbose_name_plural = 'Варианты вопросов'
