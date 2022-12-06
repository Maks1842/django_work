from rest_framework import serializers
from ..app_models.question_values import Question_Values


class Question_ValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question_Values
        fields = ['id', 'value_name',  'name_alternativ']