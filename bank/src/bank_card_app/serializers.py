from bank_card_app.models import BankCard
from rest_framework import serializers


class BankCardShortDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified bank card.
    This serializer provides short information about bank card.
    '''

    class Meta:
        model = BankCard
        fields = ['id', 'number', 'bank_account']
        read_only_fields = ['id', 'number', 'bank_account']
