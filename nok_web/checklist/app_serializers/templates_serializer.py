from rest_framework import serializers
from ..app_models.templates import Templates


class TemplatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Templates
        fields = ['id', 'name', 'type_organisations', 'template_file', 'version', 'is_deleted']