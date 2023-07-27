from rest_framework import serializers
from ..app_models.districts import Districts


class DistrictsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Districts
        fields = ['id', 'name', 'code', 'regions', 'is_deleted']
