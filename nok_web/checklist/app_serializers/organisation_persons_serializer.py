from rest_framework import serializers
from ..app_models.organisation_persons import Organisation_Persons


class Organisation_PersonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation_Persons
        fields = ['id', 'first_name', 'second_name', 'last_name', 'position', 'phone', 'email', 'organisation', 'is_deleted']