from rest_framework import serializers
from ..app_models.recommendations import Recommendations


class RecommendationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendations
        fields = ['id', 'name', 'id_type_departments', 'id_questions', 'is_deleted']