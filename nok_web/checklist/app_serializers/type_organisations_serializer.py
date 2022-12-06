from rest_framework import serializers
from ..app_models.type_organisations import Type_Organisations


class Type_OrganisationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type_Organisations
        fields = ['id', 'type', 'is_deleted']