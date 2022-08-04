from django.db import models
from django.urls import reverse

class Region(models.Model):
    region = models.CharField(max_length=50, verbose_name='Регион')  #  verbose_name - Как поле будет отображаться в админке

    def get_absolute_url(self):
        return reverse('home', kwargs={"pk": self.pk})

    def __str__(self):
        return self.region

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'


class Department(models.Model):
    name_of_department = models.CharField(max_length=100, verbose_name='Департамент')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    tel = models.CharField(max_length=15, verbose_name='Телефон')
    website = models.CharField(max_length=30, verbose_name='Сайт')
    email = models.EmailField(max_length=50, verbose_name='Email')
    fio_responsible = models.CharField(max_length=50, verbose_name='Ответственное лицо')
    region_id = models.ForeignKey('Region', on_delete=models.PROTECT, null=True, verbose_name='Регион_id')              #Поле для связывания моделей (в данном случае для модели Region)

    def get_absolute_url(self):
        return reverse('library', kwargs={"pk": self.pk})

    def __str__(self):
        return self.name_of_department

    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'


    ### ref_employee= models.ForeignKey('self',null=True,blank=True)   - пример для отношения к самому себе