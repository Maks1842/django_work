from django.db import models

'''
Информация о представителе проверяемой организации.
Данные может вносить любой пользователь приложения, как на этапе подготовки проверки
так и во время проверки.
constraints[] - позволяет проверять уникальность добавляемой записи.
'''
class Organisation_Persons(models.Model):
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    second_name = models.CharField(max_length=20, blank=True, verbose_name='Отчество')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    position = models.CharField(max_length=200, verbose_name='Должность')
    phone = models.CharField(max_length=15, blank=True, verbose_name='Телефон')
    email = models.CharField(max_length=50, blank=True, verbose_name='Email')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def __str__(self):
        name = f"{self.last_name} {self.first_name} {self.second_name or ''}"
        return name

    class Meta:
        verbose_name = 'Ответственный из Учреждения'
        verbose_name_plural = 'Ответственные из Учреждений'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "first_name",
                    "second_name",
                    "last_name",
                    "position",
                    "phone",
                    "email",
                ],
                name="unique_person")
        ]
