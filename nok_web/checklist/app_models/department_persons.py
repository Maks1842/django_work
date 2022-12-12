from django.db import models


class Department_Persons(models.Model):
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    second_name = models.CharField(max_length=20, blank=True, verbose_name='Отчество')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    position = models.CharField(max_length=200, verbose_name='Должность')
    phone = models.CharField(max_length=15, blank=True, verbose_name='Телефон')
    email = models.CharField(max_length=50, blank=True, verbose_name='Email')
    department = models.ForeignKey('Departments', on_delete=models.PROTECT, null=True, verbose_name='Департамент')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def __str__(self):
        name = f"{self.last_name} {self.first_name} {self.second_name or ''}"
        return name

    class Meta:
        verbose_name = 'Ответственный из Департамента'
        verbose_name_plural = 'Ответственные из Департаментов'