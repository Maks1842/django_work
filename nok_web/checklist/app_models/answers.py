from django.db import models

'''
Хранятся json структуры ответов на вопросы Акта, полученные в ходе заполнения экспертом/ползователем акта проверки.
Идентификация по названию проверки и названию проверяемой организации.
'''


class Answers(models.Model):
    organisations = models.ForeignKey('Organisations', on_delete=models.PROTECT, null=True, verbose_name='Организации')
    type_organisations = models.ForeignKey('Type_Organisations', on_delete=models.PROTECT, null=True, verbose_name='Тип учреждения')
    checking = models.ForeignKey('Checking', on_delete=models.PROTECT, null=True, verbose_name='Проверка')
    answers_json = models.JSONField(null=True, verbose_name='Результаты ответов')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    class Meta:
        verbose_name_plural = 'Ответы - факт'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organisations",
                    "type_organisations",
                    "checking",
                ],
                name="unique_answers")
        ]
