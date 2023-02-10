from rest_framework import serializers
from ..app_models.checking import Checking


class CheckingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checking
        fields = ['id', 'name', 'date_checking', 'region', 'department', 'finished', 'is_deleted']