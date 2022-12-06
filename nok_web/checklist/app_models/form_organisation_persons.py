from django.db import models

'''
Сопоставление проверяемой организации с представителем данной организации.
constraints[] - позволяет проверять уникальность добавляемой записи.
'''


class Form_Organisation_Persons(models.Model):
    organisation = models.ForeignKey('Organisations', on_delete=models.PROTECT, null=True, verbose_name='Учреждение')
    person = models.ForeignKey('Organisation_Persons', on_delete=models.PROTECT, null=True,
                               verbose_name='Ответственный')

    class Meta:
        verbose_name = 'Сопоставление Ответственный --> Учреждение'
        verbose_name_plural = 'Сопоставление Ответственный --> Учреждение'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organisation",
                    "person",
                ],
                name="unique_entry")
        ]
