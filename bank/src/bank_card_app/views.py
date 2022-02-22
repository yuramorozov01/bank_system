from datetime import datetime, timedelta, timezone

import jwt
from bank_card_app.models import BankCard
from bank_card_app.permissions import IsAuthenticatedBankCardOrCanViewBankCard
from bank_card_app.serializers import BankCardShortDetailsSerializer
from decouple import config
from django.contrib.auth.hashers import ScryptPasswordHasher
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
        Request has to contain POST params `number` and `pin`.
    '''

    def get_queryset(self):
        querysets_dict = {
            'retrieve': BankCard.objects.all(),
            'auth': BankCard.objects.all(),
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
