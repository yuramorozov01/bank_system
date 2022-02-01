from datetime import timedelta
from rest_framework import serializers

from deposit_app.models import DepositType, DepositContract


class DepositTypeCreateSerializer(serializers.ModelSerializer):
    '''Serializer for creating and updating deposit types'''

    class Meta:
        model = DepositType
        fields = '__all__'

    def validate(self, data):
        min_downpayment = data.get('min_downpayment')
        max_downpayment = data.get('max_downpayment')
        if (min_downpayment is not None) and (max_downpayment is not None):
            if min_downpayment > max_downpayment:
                raise serializers.ValidationError({
                    'max_downpayment': 'Maximum downpayment can\'t be less than minimal downpayment',
                })
        return data


class DepositTypeDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified deposit type.
    This serializer provides detailed information about deposit type.
    '''

    class Meta:
        model = DepositType
        fields = '__all__'
        read_only_fields = ['name', 'percent', 'deposit_term', 'currency', 'min_downpayment', 'max_downpayment',
                            'is_revocable']


class DepositTypeShortDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified deposit type.
    This serializer provides short information about deposit type.
    '''

    class Meta:
        model = DepositType
        fields = ['name', 'currency', 'deposit_term', 'is_revocable']
        read_only_fields = ['name', 'currency', 'deposit_term', 'is_revocable']


class DepositContractCreateSerializer(serializers.ModelSerializer):
    '''Serializer for creating and updating deposit contracts'''

    class Meta:
        model = DepositContract
        fields = '__all__'

    def validate(self, data):
        starts_at = data.get('starts_at')
        ends_at = data.get('ends_at')
        deposit_type = data.get('deposit_type')
        if (starts_at is not None) and (ends_at is not None):
            if starts_at > ends_at:
                raise serializers.ValidationError({
                    'starts_at': 'Start date can\'t be after end date!',
                    'ends_at': 'End date can\'t be before start date!',
                })
            if deposit_type is not None:
                real_ends_at = starts_at + timedelta(days=deposit_type.deposit_term)
                if ends_at != real_ends_at:
                    raise serializers.ValidationError({
                        'ends_at': 'Specify correct end date! It is has to be start date plus deposit term!',
                    })
        return data


class DepositContractDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified deposit contract.
    This serializer provides detailed information about deposit contract.
    '''

    class Meta:
        model = DepositContract
        fields = '__all__'
        read_only_fields = ['deposit_type', 'starts_at', 'ends_at', 'deposit_amount', 'client']


class DepositContractShortDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified deposit type.
    This serializer provides short information about deposit contract.
    '''

    class Meta:
        model = DepositContract
        fields = ['deposit_type', 'starts_at', 'ends_at', 'deposit_amount', 'client']
        read_only_fields = ['deposit_type', 'starts_at', 'ends_at', 'deposit_amount', 'client']
