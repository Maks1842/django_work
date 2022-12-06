from rest_framework import serializers
from ..app_models.form_sections import Form_Sections


class Form_SectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form_Sections
        fields = ['id', 'name', 'version', 'order_num', 'parent', 'type_departments', 'is_deleted']