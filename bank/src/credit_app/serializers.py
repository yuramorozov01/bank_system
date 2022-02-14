from datetime import timedelta

from bank_account_app.serializers import BankAccountShortDetailsSerializer
from client_app.serializers import ClientShortDetailsSerializer
from credit_app.models import CreditContract, CreditType
from rest_framework import serializers


class CreditTypeCreateSerializer(serializers.ModelSerializer):
    '''Serializer for creating and updating credit types'''

    class Meta:
        model = CreditType
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


class CreditTypeDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified credit type.
    This serializer provides detailed information about credit type.
    '''

    class Meta:
        model = CreditType
        fields = '__all__'
        read_only_fields = ['id', 'name', 'percent', 'credit_term', 'currency', 'min_downpayment', 'max_downpayment',
                            'is_annuity_payment']


class CreditTypeShortDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified credit type.
    This serializer provides short information about credit type.
    '''

    class Meta:
        model = CreditType
        fields = ['id', 'name', 'percent', 'currency', 'credit_term', 'is_annuity_payment']
        read_only_fields = ['id', 'name', 'percent', 'currency', 'credit_term', 'is_annuity_payment']


class CreditContractCreateSerializer(serializers.ModelSerializer):
    '''Serializer for creating and updating credit contracts.
    Validation of bank and credit bank accounts requires objects of bank and credit bank accounts
        in context of serializer.
    '''

    class Meta:
        model = CreditContract
        fields = '__all__'
        read_only_fields = ['is_ended', 'main_bank_account', 'credit_bank_account', 'special_bank_account']

    def validate(self, data):
        data = self.validate_start_end_dates(data)
        data = self.validate_bank_accounts(data)
        data = self.validate_credit_amount_custom(data)
        return data

    def validate_start_end_dates(self, data):
        starts_at = data.get('starts_at')
        ends_at = data.get('ends_at')
        credit_type = data.get('credit_type')
        if (starts_at is not None) and (ends_at is not None):

            # Check if start date is earlier than end data.
            if starts_at > ends_at:
                raise serializers.ValidationError({
                    'starts_at': 'Start date can\'t be after end date!',
                    'ends_at': 'End date can\'t be before start date!',
                })

            # Check if end date is after specified in credit type days
            if credit_type is not None:
                real_ends_at = starts_at + timedelta(days=(credit_type.credit_term - 1))
                if ends_at != real_ends_at:
                    raise serializers.ValidationError({
                        'ends_at': 'Specify correct end date! It is has to be start date plus credit term!',
                    })
        return data

    def validate_bank_accounts(self, data):
        main_bank_account = self.context.get('main_bank_account')
        credit_bank_account = self.context.get('credit_bank_account')
        if (main_bank_account is not None) and (credit_bank_account is not None):

            # Check that main bank account is not equal to credit bank account
            if main_bank_account == credit_bank_account:
                raise serializers.ValidationError({
                    'main_bank_account': 'Main bank account can\'t be equal to credit bank account!',
                    'credit_bank_account': 'Credit bank account can\'t be equal to main bank account!',
                })
            client = data.get('client')
            if client is not None:

                # Check if client is the same as in credit contract and main bank account and credit bank account
                if client != main_bank_account.client:
                    raise serializers.ValidationError({
                        'main_bank_account': 'Client of credit contract has to be equal to client of '
                                             'main bank account',
                    })
                if client != credit_bank_account.client:
                    raise serializers.ValidationError({
                        'credit_bank_account': 'Client of credit contract has to be equal to client of '
                                               'credit bank account',
                    })
            credit_amount = data.get('credit_amount')
            if credit_amount is not None:
                special_bank_account = self.context.get('special_bank_account')
                if special_bank_account is not None:
                    # Check if bank has enough money on his special bank account
                    if special_bank_account.balance < credit_amount:
                        raise serializers.ValidationError({
                            'credit_amount': 'Not enough money on special bank account!',
                        })
        return data

    def validate_credit_amount_custom(self, data):
        credit_amount = data.get('credit_amount')
        credit_type = data.get('credit_type')
        if (credit_amount is not None) and (credit_type is not None):
            # Check if credit amount is less than minimal downpayment of specified credit type
            if credit_amount < credit_type.min_downpayment:
                raise serializers.ValidationError({
                    'credit_amount': 'Credit amount is too low!',
                })

            # Check if credit amount is more than maximum downpayment of specified credit type
            if credit_type.max_downpayment is not None:
                if credit_amount > credit_type.max_downpayment:
                    raise serializers.ValidationError({
                        'credit_amount': 'Credit amount is too big!',
                    })
        return data


class CreditContractDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified credit contract.
    This serializer provides detailed information about credit contract.
    '''

    credit_type = CreditTypeShortDetailsSerializer(read_only=True)
    client = ClientShortDetailsSerializer(read_only=True)
    main_bank_account = BankAccountShortDetailsSerializer(read_only=True)
    credit_bank_account = BankAccountShortDetailsSerializer(read_only=True)
    special_bank_account = BankAccountShortDetailsSerializer(read_only=True)

    class Meta:
        model = CreditContract
        fields = '__all__'
        read_only_fields = ['id', 'credit_type', 'starts_at', 'ends_at', 'is_ended', 'credit_amount', 'client',
                            'main_bank_account', 'credit_bank_account', 'special_bank_account']


class CreditContractShortDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified credit contract.
    This serializer provides short information about credit contract.
    '''

    client = ClientShortDetailsSerializer(read_only=True)
    credit_type = CreditTypeShortDetailsSerializer(read_only=True)

    class Meta:
        model = CreditContract
        fields = ['id', 'credit_type', 'starts_at', 'ends_at', 'is_ended', 'credit_amount', 'client']
        read_only_fields = ['id', 'credit_type', 'starts_at', 'ends_at', 'is_ended', 'credit_amount', 'client']
