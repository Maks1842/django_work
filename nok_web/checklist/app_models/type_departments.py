from django.db import models


'''
Хранятся типы департаментов (Культура, Образование и т.д.).
'''
class Type_Departments(models.Model):
    type = models.CharField(max_length=100, verbose_name='Тип департамента')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Тип департамента'
        verbose_name_plural = 'Типы департаментов'