from rest_framework import serializers
from ..app_models.comments import Comments


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'free_value', 'is_deleted']