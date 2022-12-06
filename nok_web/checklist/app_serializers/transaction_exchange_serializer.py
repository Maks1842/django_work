from rest_framework import serializers
from ..app_models.transaction_exchange import Transaction_Exchange


class Transaction_ExchangeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Transaction_Exchange
        fields = ['id', 'model', 'field', 'old_data', 'new_data', 'date_exchange', 'user']