from datetime import timedelta

from bank_account_app.serializers import BankAccountShortDetailsSerializer
from deposit_app.models import DepositContract, DepositType
from rest_framework import serializers


class DepositTypeCreateSerializer(serializers.ModelSerializer):
    '''Serializer for creating and updating deposit types'''

    class Meta:
        model = DepositType
        fields = '__all__'

    def validate(self, data):
        min_downpayment = data.get('min_downpayment')
        max_downpayment = data.get('max_downpayment')
        if (min_downpayment is not None) and (max_downpayment is not None):

            # Check if maximum downpayment is less than minimal downpayment
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
        read_only_fields = ['id', 'name', 'percent', 'deposit_term', 'currency', 'min_downpayment', 'max_downpayment',
                            'is_revocable']


class DepositTypeShortDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified deposit type.
    This serializer provides short information about deposit type.
    '''

    class Meta:
        model = DepositType
        fields = ['id', 'name', 'currency', 'deposit_term', 'is_revocable']
        read_only_fields = ['id', 'name', 'currency', 'deposit_term', 'is_revocable']


class DepositContractCreateSerializer(serializers.ModelSerializer):
    '''Serializer for creating and updating deposit contracts.
    Validation of bank and deposit bank accounts requires objects of bank and deposit bank accounts
        in context of serializer.
    '''

    class Meta:
        model = DepositContract
        fields = '__all__'
        read_only_fields = ['main_bank_account', 'deposit_bank_account']

    def validate(self, data):
        data = self.validate_start_end_dates(data)
        data = self.validate_bank_accounts(data)
        return data

    def validate_start_end_dates(self, data):
        starts_at = data.get('starts_at')
        ends_at = data.get('ends_at')
        deposit_type = data.get('deposit_type')
        if (starts_at is not None) and (ends_at is not None):

            # Check if start date is earlier than end data.
            if starts_at > ends_at:
                raise serializers.ValidationError({
                    'starts_at': 'Start date can\'t be after end date!',
                    'ends_at': 'End date can\'t be before start date!',
                })

            # Check if end date is after specified in deposit type days
            if deposit_type is not None:
                real_ends_at = starts_at + timedelta(days=deposit_type.deposit_term)
                if ends_at != real_ends_at:
                    raise serializers.ValidationError({
                        'ends_at': 'Specify correct end date! It is has to be start date plus deposit term!',
                    })
        return data

    def validate_bank_accounts(self, data):
        main_bank_account = self.context.get('main_bank_account')
        deposit_bank_account = self.context.get('deposit_bank_account')
        if (main_bank_account is not None) and (deposit_bank_account is not None):

            # Check that main bank account is not equal to deposit bank account
            if main_bank_account == deposit_bank_account:
                raise serializers.ValidationError({
                    'main_bank_account': 'Main bank account can\'t be equal to deposit bank account!',
                    'deposit_bank_account': 'Deposit bank account can\'t be equal to main bank account!',
                })
            client = data.get('client')
            if client is not None:

                # Check if client is the same as in deposit contract and main bank account and deposit bank account
                if client != main_bank_account.client:
                    raise serializers.ValidationError({
                        'main_bank_account': 'Client of deposit contract has to be equal to client of '
                                             'main bank account',
                    })
                if client != deposit_bank_account.client:
                    raise serializers.ValidationError({
                        'deposit_bank_account': 'Client of deposit contract has to be equal to client of '
                                                'deposit bank account',
                    })
            deposit_amount = data.get('deposit_amount')
            if deposit_amount is not None:

                # Check if client has enough money on his main bank account
                if main_bank_account.balance < deposit_amount:
                    raise serializers.ValidationError({
                        'deposit_amount': 'Not enough money on main bank account!',
                    })
        return data


class DepositContractDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified deposit contract.
    This serializer provides detailed information about deposit contract.
    '''

    main_bank_account = BankAccountShortDetailsSerializer(read_only=True)
    deposit_bank_account = BankAccountShortDetailsSerializer(read_only=True)

    class Meta:
        model = DepositContract
        fields = '__all__'
        read_only_fields = ['id', 'deposit_type', 'starts_at', 'ends_at', 'deposit_amount', 'client',
                            'main_bank_account', 'deposit_bank_account']


class DepositContractShortDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified deposit type.
    This serializer provides short information about deposit contract.
    '''

    class Meta:
        model = DepositContract
        fields = ['id', 'deposit_type', 'starts_at', 'ends_at', 'deposit_amount', 'client']
        read_only_fields = ['id', 'deposit_type', 'starts_at', 'ends_at', 'deposit_amount', 'client']
