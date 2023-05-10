# Generated by Django 4.0.5 on 2023-04-05 05:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0057_alter_answers_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list_checking',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='checklist.organisation_persons', verbose_name='Ответственный'),
        ),
    ]