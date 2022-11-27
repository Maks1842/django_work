# Generated by Django 4.0.5 on 2022-11-25 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0022_remove_answers_free_value_alter_templates_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='templates',
            name='type_organisations',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='checklist.type_organisations', verbose_name='Тип учреждения'),
        ),
        migrations.AlterField(
            model_name='organisation_persons',
            name='organisation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='checklist.organisations', verbose_name='Учреждение'),
        ),
        migrations.AlterField(
            model_name='templates',
            name='version',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='checklist.versions', verbose_name='Версия'),
        ),
    ]