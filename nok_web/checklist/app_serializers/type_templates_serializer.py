from rest_framework import serializers
from ..app_models.type_templates import Type_Templates


class Type_TemplatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type_Templates
        fields = ['id', 'type']