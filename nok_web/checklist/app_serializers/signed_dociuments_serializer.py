from rest_framework import serializers
from ..app_models.signed_dociuments import Signed_Dociuments


class Signed_DociumentsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Signed_Dociuments
        fields = ['id', 'file_name', 'originat_file_name', 'description', 'created_at', 'is_deleted', 'user']