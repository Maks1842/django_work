# Generated by Django 4.0.5 on 2022-11-10 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0014_alter_form_sections_question_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questions',
            old_name='name',
            new_name='questions',
        ),
        migrations.RemoveField(
            model_name='questions',
            name='answer_variant',
        ),
        migrations.RemoveField(
            model_name='questions',
            name='form_sections',
        ),
        migrations.RemoveField(
            model_name='questions',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='questions',
            name='type_answers',
        ),
        migrations.RemoveField(
            model_name='questions',
            name='type_organisations',
        ),
    ]
