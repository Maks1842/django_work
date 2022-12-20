from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, verbose_name='Пользователь')
    phone = models.CharField(max_length=30, blank=True, verbose_name='Телефон')
    address = models.CharField(max_length=100, blank=True, verbose_name='Адрес')
    birthday = models.DateField(null=True, verbose_name='Дата рождения')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'birthday',
                ],
                name="profile")
        ]