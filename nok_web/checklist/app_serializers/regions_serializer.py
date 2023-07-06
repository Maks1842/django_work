from rest_framework import serializers
from ..app_models.regions import Regions


class RegionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regions
        fields = ['id', 'region_name', 'is_deleted']
