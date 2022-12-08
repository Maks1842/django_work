from rest_framework import serializers
from ..app_models.photo import Photo


class PhotoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Photo
        fields = ['id', 'file_name', 'original_file_name', 'description', 'created_at', 'is_deleted', 'user']