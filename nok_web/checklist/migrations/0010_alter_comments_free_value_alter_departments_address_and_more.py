# Generated by Django 4.0.5 on 2022-10-08 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0009_alter_questions_answer_variant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='free_value',
            field=models.CharField(max_length=500, verbose_name='Комментарии'),
        ),
        migrations.AlterField(
            model_name='departments',
            name='address',
            field=models.CharField(max_length=300, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='departments',
            name='website',
            field=models.CharField(max_length=50, verbose_name='Сайт'),
        ),
        migrations.AlterField(
            model_name='forms',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Наименование формы Акта/Отчета'),
        ),
        migrations.AlterField(
            model_name='forms_recommendations',
            name='free_value',
            field=models.CharField(max_length=500, verbose_name='Рекомендации в свободной форме'),
        ),
        migrations.AlterField(
            model_name='organisations',
            name='address',
            field=models.CharField(max_length=300, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='question_values',
            name='value_name',
            field=models.CharField(max_length=500, verbose_name='Варианты ответов'),
        ),
        migrations.AlterField(
            model_name='questions',
            name='name',
            field=models.CharField(max_length=2000, verbose_name='Вопросы'),
        ),
        migrations.AlterField(
            model_name='regions',
            name='region_name',
            field=models.CharField(max_length=100, verbose_name='Регион'),
        ),
        migrations.AlterField(
            model_name='templates',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Наименование шаблона html'),
        ),
        migrations.AlterField(
            model_name='transaction_exchange',
            name='new_data',
            field=models.CharField(max_length=2000, verbose_name='Новые данные'),
        ),
        migrations.AlterField(
            model_name='transaction_exchange',
            name='old_data',
            field=models.CharField(max_length=2000, verbose_name='Старые данные'),
        ),
        migrations.AlterField(
            model_name='type_departments',
            name='type',
            field=models.CharField(max_length=100, verbose_name='Тип департамента'),
        ),
        migrations.AlterField(
            model_name='type_organisations',
            name='type',
            field=models.CharField(max_length=100, verbose_name='Тип учреждения'),
        ),
    ]
