from bank_account_app.models import BankAccount
from bank_account_app.permissions import IsUserManagerViewBankAccount
from bank_account_app.serializers import (BankAccountDetailsSerializer,
                                          BankAccountShortDetailsSerializer)
from django.db import transaction
from django.db.models import F
from rest_framework import permissions, validators, viewsets
from rest_framework.decorators import action


class BankAccountViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    retrieve:
        Get the specified bank account.
    list:
        Get a list of all bank accounts.
    '''

    def get_queryset(self):
        querysets_dict = {
            'retrieve': BankAccount.objects.all(),
            'list': BankAccount.objects.all(),
            'top_up': BankAccount.objects.all(),
        }
        queryset = querysets_dict.get(self.action)
        return queryset.distinct()

    def get_serializer_class(self):
        serializers_dict = {
            'retrieve': BankAccountDetailsSerializer,
            'list': BankAccountShortDetailsSerializer,
            'top_up': BankAccountDetailsSerializer,
        }
        serializer_class = serializers_dict.get(self.action)
        return serializer_class

    def get_permissions(self):
        base_permissions = [permissions.IsAuthenticated, IsUserManagerViewBankAccount]
        permissions_dict = {
            'retrieve': [],
            'list': [],
            'top_up': [],
        }
        base_permissions += permissions_dict.get(self.action, [])
        return [permission() for permission in base_permissions]

    @action(methods=['PATCH'], detail=True)
    def top_up(self, request, pk=None):
        # Top up balance to bank account
        try:
            bank_account = BankAccount.objects.get(pk=pk)
            amount = self.request.POST.get('amount')
            self.validate_top_up_amount(amount)

            with transaction.atomic():
                bank_account.balance = F('balance') + amount
                bank_account.save()
            return self.retrieve(request, pk=pk)
            # queryset = self.get_queryset()
            # serializer = self.get_serializer_class()(queryset)
            # return Response(serializer.data)
        except BankAccount.DoesNotExist:
            raise validators.ValidationError({
                'bank_account': 'Bank account with specified id doesn\'t exists!',
            })

    def validate_top_up_amount(self, value):
        if value is None:
            raise validators.ValidationError({
                'amount': 'This field is required!'
            })

        int_value = 0
        try:
            int_value = int(value)
        except ValueError:
            raise validators.ValidationError({
                'amount': 'Incorrect value!'
            })

        if int_value < 0:
            raise validators.ValidationError({
                'amount': 'This field is has to be positive!'
            })
