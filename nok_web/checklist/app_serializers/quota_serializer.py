from rest_framework import serializers
from ..app_models.quota import Quota


class QuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quota
        fields = ['id', 'quota']