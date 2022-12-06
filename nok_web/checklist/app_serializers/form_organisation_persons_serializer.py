from rest_framework import serializers
from ..app_models.form_organisation_persons import Form_Organisation_Persons


class Form_Organisation_PersonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form_Organisation_Persons
        fields = ['id', 'organisation', 'person']