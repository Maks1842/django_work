from rest_framework import serializers
from ..app_models.department_persons import Department_Persons


class Department_PersonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department_Persons
        fields = ['id', 'first_name', 'second_name', 'last_name', 'position', 'phone', 'email', 'department', 'is_deleted']