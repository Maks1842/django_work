from rest_framework import serializers
from ..app_models.organisations import Organisations


class OrganisationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisations
        fields = ['id', 'organisation_name', 'address', 'phone', 'website', 'email', 'parent', 'department', 'is_deleted']