from django.db import models

'''
Хранятся типы проверяемых учреждений (Амбулатория, ДОУ, ОО, Здание культурного наследия и т.п.).
'''


class Type_Organisations(models.Model):
    type = models.CharField(max_length=100, verbose_name='Тип учреждения')
    type_departments = models.ForeignKey('Type_Departments', on_delete=models.PROTECT, null=True,
                                         verbose_name='Тип департамента')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Тип учреждения'
        verbose_name_plural = 'Типы учреждений'
