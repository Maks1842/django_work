from rest_framework import serializers
from ..app_models.form_type_organisation import Form_Type_Organisation


class Form_Type_OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form_Type_Organisation
        fields = ['id', 'organisation', 'type_organisation']