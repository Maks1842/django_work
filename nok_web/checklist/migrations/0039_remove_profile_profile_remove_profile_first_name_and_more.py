# Generated by Django 4.0.5 on 2022-12-20 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0038_profile_profile_profile'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='profile',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='second_name',
        ),
        migrations.AddConstraint(
            model_name='profile',
            constraint=models.UniqueConstraint(fields=('user', 'birthday'), name='profile'),
        ),
    ]
