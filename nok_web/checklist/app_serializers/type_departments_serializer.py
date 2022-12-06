from rest_framework import serializers
from ..app_models.type_departments import Type_Departments


class Type_DepartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type_Departments
        fields = ['id', 'type', 'is_deleted']