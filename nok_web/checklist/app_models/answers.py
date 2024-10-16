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
    quota = models.IntegerField(default=1, verbose_name='Количество получателей услуг')
    invalid_person = models.IntegerField(null=True, blank=True, verbose_name='Количество инвалидов')
    comments = models.CharField(max_length=500, blank=True, verbose_name='Комментарий эксперта')
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
