from rest_framework import serializers
from ..app_models.coefficients import Coefficients


class CoefficientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coefficients
        fields = ['id', 'type_departments', 'type_organisations', 'main_json', 'respondents_json', 'points_json', 'date', 'version']