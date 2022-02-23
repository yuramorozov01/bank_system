from bank_card_app.models import BankCard
from rest_framework import serializers


class BankCardShortDetailsSerializer(serializers.ModelSerializer):
    '''
    Serializer for a specified bank card.
    This serializer provides short information about bank card.
    '''

    class Meta:
        model = BankCard
        fields = ['id', 'number', 'bank_account']
        read_only_fields = ['id', 'number', 'bank_account']


class AccesJWTSerializer(serializers.Serializer):
    '''Serializer for access JWT to authenticate bank card'''
    access = serializers.CharField(max_length=4096)


class ReceiptSerializer(serializers.Serializer):
    '''Serializer for a receipt of bank operation.'''

    time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S %Z', read_only=True)
    value = serializers.DecimalField(max_digits=21, decimal_places=2, read_only=True)
    bank_card_number = serializers.CharField(max_length=16, min_length=16, read_only=True)
