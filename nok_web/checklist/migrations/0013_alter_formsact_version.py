# Generated by Django 4.0.5 on 2022-11-08 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0012_listforcheck_formsact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formsact',
            name='version',
            field=models.CharField(default=1, max_length=50, verbose_name='Версия формы акта'),
            preserve_default=False,
        ),
    ]
