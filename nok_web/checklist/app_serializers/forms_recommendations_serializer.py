from rest_framework import serializers
from ..app_models.forms_recommendations import Forms_Recommendations


class Forms_RecommendationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forms_Recommendations
        fields = ['id', 'free_value', 'answers', 'form_sections', 'recommendations', 'is_deleted']