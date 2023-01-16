# Generated by Django 4.0.5 on 2023-01-16 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0042_form_sections_question_required'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile_Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=100, verbose_name='Должность')),
            ],
            options={
                'verbose_name_plural': 'Должности',
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='checklist.profile_position', verbose_name='Должность'),
        ),
    ]