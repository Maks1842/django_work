from rest_framework import serializers
from ..app_models.departments import Departments


class DepartmentsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Departments
        fields = ['id', 'department_name', 'address', 'phone', 'website', 'email', 'parent', 'region', 'type_departments', 'is_deleted', 'user']