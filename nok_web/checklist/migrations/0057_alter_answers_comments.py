# Generated by Django 4.0.5 on 2023-03-21 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0056_answers_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answers',
            name='comments',
            field=models.CharField(blank=True, default=1, max_length=500, verbose_name='Комментарий эксперта'),
            preserve_default=False,
        ),
    ]
