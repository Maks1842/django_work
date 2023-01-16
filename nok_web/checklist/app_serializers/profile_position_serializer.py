from rest_framework import serializers

from ..app_models import Profile_Position


class Profile_PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile_Position
        fields = ['id', 'position']