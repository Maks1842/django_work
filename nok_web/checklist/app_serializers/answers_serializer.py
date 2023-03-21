from rest_framework import serializers
from ..app_models.answers import Answers


class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ['id', 'organisations', 'type_organisations',  'checking', 'answers_json', 'quota', 'invalid_person', 'comments', 'is_deleted']