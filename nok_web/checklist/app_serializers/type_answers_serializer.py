from rest_framework import serializers
from ..app_models.type_answers import Type_Answers


class Type_AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type_Answers
        fields = ['id', 'type']