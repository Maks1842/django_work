from rest_framework import serializers
from ..app_models.list_checking import List_Checking


class ListCheckingSerializer(serializers.ModelSerializer):
    class Meta:
        model = List_Checking
        fields = ['id', 'checking', 'organisation', 'person', 'user', 'date_check_org', 'is_deleted']