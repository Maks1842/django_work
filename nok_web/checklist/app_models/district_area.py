from django.db import models


class DistrictArea(models.Model):
    data = models.JSONField(null=True, verbose_name='Результаты')
