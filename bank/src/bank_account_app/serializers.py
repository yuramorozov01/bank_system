from bank_account_app.models import BankAccount
from client_app.serializers import ClientShortDetailsSerializer
from rest_framework import serializers


class BankAccountDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified bank account.
    This serializer provides detailed information about bank account.
    '''

    client = ClientShortDetailsSerializer(read_only=True)

    class Meta:
        model = BankAccount
        fields = '__all__'
        read_only_fields = ['id', 'number', 'activity_type', 'bank_account_type', 'balance', 'client']


class BankAccountShortDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified deposit type.
    This serializer provides short information about deposit contract.
    '''

    client = ClientShortDetailsSerializer(read_only=True)

    class Meta:
        model = BankAccount
        fields = ['id', 'number', 'activity_type', 'bank_account_type', 'balance', 'client']
        read_only_fields = ['id', 'number', 'activity_type', 'bank_account_type', 'balance', 'client']


class EmptyBankAccountSerializer(serializers.ModelSerializer):
    '''Empty serializer.
    To use GenericViewSet (GenericAPIView requires get_queryset() and get_serializer_class() methods).
    '''

    class Meta:
        model = BankAccount
        fields = []
