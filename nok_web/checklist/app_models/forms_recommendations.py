from django.db import models

'''
Хранятся рекомендации в свободной форме по замечаниям отраженным в акте проверки.
Данные этой модели используются при составлении итоговых отчетов.
'''


class Forms_Recommendations(models.Model):
    free_value = models.CharField(max_length=500, verbose_name='Рекомендации в свободной форме')
    answers = models.ForeignKey('Answers', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Ответы')
    form_sections = models.ForeignKey('Form_Sections', on_delete=models.PROTECT, null=True, blank=True,
                                      verbose_name='Разделы')
    recommendations = models.ForeignKey('Recommendations', on_delete=models.PROTECT, null=True, blank=True,
                                        verbose_name='Рекоммендации')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    class Meta:
        verbose_name_plural = 'Рекомендации - факт'
