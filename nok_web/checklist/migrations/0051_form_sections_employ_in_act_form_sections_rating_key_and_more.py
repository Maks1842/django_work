# Generated by Django 4.0.5 on 2023-02-14 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0050_checking_finished'),
    ]

    operations = [
        migrations.AddField(
            model_name='form_sections',
            name='employ_in_act',
            field=models.BooleanField(default=False, verbose_name='Признак использования в Акте'),
        ),
        migrations.AddField(
            model_name='form_sections',
            name='rating_key',
            field=models.CharField(blank=True, max_length=20, verbose_name='Ключ для рейтингов'),
        ),
        migrations.AlterField(
            model_name='form_sections',
            name='order_num',
            field=models.IntegerField(blank=True, null=True, verbose_name='Порядковый номер'),
        ),
        migrations.CreateModel(
            name='Coefficients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_json', models.JSONField(blank=True, verbose_name='Коэффициенты законодательные')),
                ('respondents_json', models.JSONField(blank=True, verbose_name='Коэффициенты рандомные, для респондентов')),
                ('points_json', models.JSONField(blank=True, verbose_name='Баллы законодательные')),
                ('date', models.DateField(blank=True, verbose_name='Дата коэффициентов')),
                ('version', models.CharField(max_length=50, verbose_name='Версия коэффициентов')),
                ('type_departments', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='checklist.type_departments', verbose_name='Тип департамента')),
                ('type_organisations', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='checklist.type_organisations', verbose_name='Тип учреждения')),
            ],
            options={
                'verbose_name_plural': 'Коэффициенты для рейтингов',
            },
        ),
    ]
