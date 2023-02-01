from rest_framework import serializers
from ..app_models.ratings import Ratings


class RatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = ['id', 'organisations', 'type_organisations',  'checking', 'ratings_json', 'is_deleted']