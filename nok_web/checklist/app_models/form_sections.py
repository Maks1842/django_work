from django.db import models


class Form_Sections(models.Model):
    name = models.CharField(max_length=500, verbose_name='Наименование разделов')
    version = models.CharField(max_length=20, verbose_name='Версия раздела')
    order_num = models.IntegerField(verbose_name='Порядковый номер')
    parent = models.ForeignKey('Form_Sections', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Parent')
    type_departments = models.ForeignKey('Type_Departments', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Тип департамента')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Наименование разделов акта'
