from rest_framework import serializers
from ..app_models.questions import Questions


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ['id', 'questions']