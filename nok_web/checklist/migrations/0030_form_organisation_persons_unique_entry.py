from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0029_recommendations_id_questions_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='form_organisation_persons',
            constraint=models.UniqueConstraint(fields=('organisation', 'person'), name='unique_entry'),
        ),
    ]
