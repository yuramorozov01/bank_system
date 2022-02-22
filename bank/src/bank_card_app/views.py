from datetime import datetime, timedelta, timezone

import jwt
from bank_card_app.models import BankCard
from bank_card_app.permissions import IsAuthenticatedBankCard, IsAuthenticatedBankCardOrCanViewBankCard
from bank_card_app.serializers import BankCardShortDetailsSerializer
from decouple import config
from django.contrib.auth.hashers import ScryptPasswordHasher
from django.db import transaction
from django.db.models import F
from django.http import JsonResponse
from rest_framework import mixins, validators, viewsets
from rest_framework.decorators import action


class BankCardViewSet(mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    '''
    retrieve:
        Get the specified bank card.
    auth:
        Create JWT to authenticate bank card by bank card number and it's pin.
        Request has to contain POST params:
            `number`: bank card number
            `pin`: bank card pin
    withdraw:
        Withdraw money from bank account by authenticated bank card.
        Request has to contain POST params:
            `amount`: withdraw amount
        Returns:
            `time`: current time
            `withdraw_amount`: withdraw amount
            `bank_card_number`: bank card number
    '''

    def get_queryset(self):
        querysets_dict = {
            'retrieve': BankCard.objects.all(),
            'auth': BankCard.objects.all(),
            'withdraw': BankCard.objects.filter(number=self.request.bank_card.number),
        }
        queryset = querysets_dict.get(self.action)
        return queryset.distinct()

    def get_serializer_class(self):
        serializers_dict = {
            'retrieve': BankCardShortDetailsSerializer,
        }
        serializer_class = serializers_dict.get(self.action)
        return serializer_class

    def get_permissions(self):
        base_permissions = []
        permissions_dict = {
            'retrieve': [IsAuthenticatedBankCardOrCanViewBankCard],
            'auth': [],
            'withdraw': [IsAuthenticatedBankCard],
        }
        base_permissions += permissions_dict.get(self.action, [])
        return [permission() for permission in base_permissions]

    @action(methods=['POST'], detail=False)
    def auth(self, request):
        # Create JWT to authenticate bank card
        try:
            # Parse and validate bank card number from POST request
            bank_card_number = self.request.POST.get('number')
            if bank_card_number is None:
                raise validators.ValidationError({
                    'number': 'Specify bank card number to authenticate!',
                })

            # Parse and validate bank card pin from POST request
            pin = self.request.POST.get('pin')
            if pin is None:
                raise validators.ValidationError({
                    'pin': 'Specify bank card pin to authenticate!',
                })

            bank_card = self.get_queryset().get(number=bank_card_number)

            # Verify hashed bank card pin and pin from request
            hasher = ScryptPasswordHasher()
            if not hasher.verify(pin, bank_card.pin):
                raise validators.ValidationError({
                    'pin': 'Incorrect pin!',
                })

            # Create new access JWT with payload to authenticate bank card
            payload = {
                'bank_card_number': bank_card.number,
                'exp': datetime.now(tz=timezone.utc) + timedelta(minutes=1000),
            }
            new_access_jwt = jwt.encode(payload, config('SECRET_KEY'), algorithm='HS256')
            return JsonResponse({'access': new_access_jwt}, status=201)

        except BankCard.DoesNotExist:
            raise validators.ValidationError({
                'number': 'Bank account with specified number doesn\'t exists!',
            })

    @action(methods=['PUT', 'PATCH'], detail=False)
    def withdraw(self, request):
        # Parse and validate withdraw amount from POST request
        withdraw_amount = self.request.POST.get('amount')
        withdraw_amount = self.validate_withdraw_amount(withdraw_amount)

        # Withdraw money
        with transaction.atomic():
            bank_card = self.request.bank_card
            bank_account = bank_card.bank_account

            if withdraw_amount > bank_account.balance:
                raise validators.ValidationError({
                    'amount': 'You don\'t have enough money!'
                })

            bank_account.balance = F('balance') - withdraw_amount
            bank_account.save()

        receipt = {
            'time': datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H-%M-%S %Z'),
            'withdraw_amount': withdraw_amount,
            'bank_card_number': bank_card.number,
        }
        return JsonResponse(receipt, status=200)

    def validate_withdraw_amount(self, value):
        if value is None:
            raise validators.ValidationError({
                'amount': 'This field is required!'
            })

        try:
            float_value = float(value)
        except ValueError:
            raise validators.ValidationError({
                'amount': 'Incorrect value!'
            })

        if float_value < 0:
            raise validators.ValidationError({
                'amount': 'This field is has to be positive!'
            })
        return float_value
