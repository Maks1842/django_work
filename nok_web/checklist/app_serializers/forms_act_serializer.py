from rest_framework import serializers
from ..app_models.forms_act import FormsAct


class FormsActSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormsAct
        fields = ['id', 'type_departments', 'type_organisations', 'act_json', 'act_json_to_calculate', 'date', 'version']