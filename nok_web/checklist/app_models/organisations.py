from django.db import models


class Organisations(models.Model):
    organisation_name = models.CharField(max_length=200, verbose_name='Учреждение')
    address = models.CharField(max_length=300, blank=True, verbose_name='Юридический Адрес')
    phone = models.CharField(max_length=100, blank=True, verbose_name='Телефон')
    website = models.CharField(max_length=100, blank=True, verbose_name='Сайт')
    email = models.EmailField(max_length=100, blank=True, verbose_name='Email')
    parent = models.ForeignKey('Organisations', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Parent')
    department = models.ForeignKey('Departments', on_delete=models.PROTECT, null=True, verbose_name='Департамент')
    district = models.ForeignKey('Districts', on_delete=models.PROTECT, null=True, blank=True,
                               verbose_name='Район региона')
    inn = models.CharField(max_length=12, blank=True, verbose_name='ИНН')
    kpp = models.CharField(max_length=9, blank=True, verbose_name='КПП')
    ogrn = models.CharField(max_length=15, blank=True, verbose_name='ОГРН')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')
    latitude = models.FloatField(max_length=10, blank=True, null=True, verbose_name='Широта')
    longitude = models.FloatField(max_length=10, blank=True, null=True, verbose_name='Долгота')

    def __str__(self):
        return self.organisation_name

    class Meta:
        verbose_name = 'Учреждение'
        verbose_name_plural = 'Учреждения'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organisation_name",
                ],
                name="unique_organisations")
        ]
