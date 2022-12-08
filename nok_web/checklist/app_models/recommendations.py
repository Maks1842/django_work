from django.db import models


'''
Хранятся типовые рекомендации по замечаниям отраженным в акте проверки.
Данные этой модели используются при составлении итоговых отчетов.
'''
class Recommendations(models.Model):
    name = models.CharField(max_length=500, verbose_name='Рекоммендации')
    id_type_departments = models.CharField(max_length=20, null=True, blank=True, verbose_name='Список id департаментов')
    id_questions = models.CharField(max_length=50, null=True, blank=True, verbose_name='Список id вопросов')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Варианты рекоммендаций'