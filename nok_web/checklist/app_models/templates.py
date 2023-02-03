from django.db import models


class Templates(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование шаблона html')
    type_organisations = models.ForeignKey('Type_Organisations', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Тип учреждения')
    template_file = models.FileField(verbose_name='Ссылка на шаблон')
    type_templates = models.ForeignKey('Type_Templates', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Тип шаблона')
    version = models.ForeignKey('Versions', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Версия')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Шаблоны html'
        verbose_name_plural = 'Шаблоны html'
