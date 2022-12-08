from django.db import models


'''
Сопоставление проверяемой организации с её типом.
constraints[] - позволяет проверять уникальность добавляемой записи
'''
class Form_Type_Organisation(models.Model):
    organisation = models.ForeignKey('Organisations', on_delete=models.PROTECT, null=True, verbose_name='Учреждение')
    type_organisation = models.ForeignKey('Type_Organisations', on_delete=models.PROTECT, null=True, verbose_name='Тип учреждения')

    def __str__(self):
        name = f"{self.organisation} {self.type_organisation}"
        return name

    class Meta:
        verbose_name_plural = 'Сопоставление Учреждение --> Тип'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organisation",
                    "type_organisation",
                ],
                name="unique_typeorg")
        ]
