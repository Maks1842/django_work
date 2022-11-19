# Generated by Django 4.0.5 on 2022-11-19 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0017_checking_list_checking_delete_listforcheck'),
    ]

    operations = [
        migrations.AddField(
            model_name='type_organisations',
            name='type_departments',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='checklist.type_departments', verbose_name='Тип департамента'),
        ),
    ]
