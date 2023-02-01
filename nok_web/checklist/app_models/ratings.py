from django.db import models

'''
Хранятся json структуры Результатов рейтинговой оценки, по итогам проверки.
'''


class Ratings(models.Model):
    organisations = models.ForeignKey('Organisations', on_delete=models.PROTECT, null=True, verbose_name='Организации')
    type_organisations = models.ForeignKey('Type_Organisations', on_delete=models.PROTECT, null=True, verbose_name='Тип учреждения')
    checking = models.ForeignKey('Checking', on_delete=models.PROTECT, null=True, verbose_name='Проверка')
    ratings_json = models.JSONField(null=True, verbose_name='Результаты рейтинговой оценки')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    class Meta:
        verbose_name_plural = 'Рейтинговая оценка - ИТОГО'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organisations",
                    "type_organisations",
                    "checking",
                ],
                name="unique_ratings")
        ]
