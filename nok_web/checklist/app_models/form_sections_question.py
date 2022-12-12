from django.db import models


class Form_Sections_Question(models.Model):
    question = models.ForeignKey('Questions', on_delete=models.PROTECT, verbose_name='Вопрос')
    order_num = models.IntegerField(null=True, blank=True, verbose_name='Порядковый номер')
    form_sections = models.ForeignKey('Form_Sections', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Наименование разделов')
    type_answers = models.ForeignKey('Type_Answers', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Тип ответа')
    answer_variant = models.CharField(max_length=50, blank=True, verbose_name='Вариант ответа')
    type_organisations = models.CharField(max_length=50, null=True, blank=True, verbose_name='id Типов учреждений')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    class Meta:
        verbose_name_plural = 'Сопоставление вопрос-раздел'
