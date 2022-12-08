from django.db import models


class Quota(models.Model):
    quota = models.IntegerField(verbose_name='Квота респондентов')

    def __str__(self):
        return '{0}'.format(self.quota)

    class Meta:
        verbose_name = 'Квота'
        verbose_name_plural = 'Квоты'
