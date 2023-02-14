from django.db import models

'''
Хранятся коэффициент, используемые при расчете рейтингов.
'''


class Coefficients(models.Model):
    type_departments = models.ForeignKey('Type_Departments', on_delete=models.PROTECT, null=True,
                                         verbose_name='Тип департамента')
    type_organisations = models.ForeignKey('Type_Organisations', on_delete=models.PROTECT, null=True, blank=True,
                                           verbose_name='Тип учреждения')
    main_json = models.JSONField(null=True, blank=True, verbose_name='Коэффициенты законодательные')
    respondents_json = models.JSONField(null=True, blank=True, verbose_name='Коэффициенты рандомные, для респондентов')
    points_json = models.JSONField(null=True, blank=True, verbose_name='Баллы законодательные')
    date = models.DateField(blank=True, verbose_name='Дата коэффициентов')
    version = models.CharField(max_length=50, verbose_name='Версия коэффициентов')

    class Meta:
        verbose_name_plural = 'Коэффициенты для рейтингов'
