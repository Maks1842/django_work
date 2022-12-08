from rest_framework import serializers
from ..app_models.versions import Versions


class VersionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Versions
        fields = ['id', 'table_name', 'version', 'active', 'is_deleted']