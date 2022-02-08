from datetime import timedelta

from bank_account_app.permissions import (IsUserManagerChangeBankAccount,
                                          IsUserManagerViewBankAccount)
from bank_account_app.serializers import EmptyBankAccountSerializer
from base_app.models import BankSettings
from deposit_app.models import DepositContract
from deposit_app.permissions import (IsUserManagerChangeDepositContract,
                                     IsUserManagerViewDepositContract,
                                     IsUserManagerViewDepositType)
from deposit_app.utils import deposit_interest_accrual, deposit_withdraw
from django.db import transaction
from django.db.models import F
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class CloseDayViewSet(viewsets.GenericViewSet):
    '''
    update:
        Update bank accounts balances (with deposits and credits programs)
    partial_update:
        Update bank accounts balances (with deposits and credits programs)
    '''

    def get_queryset(self):
        querysets_dict = {
            'close_day': None,
        }
        queryset = querysets_dict.get(self.action)
        return queryset

    def get_serializer_class(self):
        serializers_dict = {
            'close_day': EmptyBankAccountSerializer,
        }
        serializer_class = serializers_dict.get(self.action)
        return serializer_class

    def get_permissions(self):
        base_permissions = [permissions.IsAuthenticated, IsUserManagerViewBankAccount,
                            IsUserManagerViewDepositType, IsUserManagerViewDepositContract]
        permissions_dict = {
            'update': [IsUserManagerChangeBankAccount, IsUserManagerChangeDepositContract],
            'partial_update': [IsUserManagerChangeBankAccount, IsUserManagerChangeDepositContract],
        }
        base_permissions += permissions_dict.get(self.action, [])
        return [permission() for permission in base_permissions]

    @action(methods=['PUT', 'PATCH'], detail=False)
    def close_day(self, request):
        with transaction.atomic():
            bank_settings, created = BankSettings.objects.get_or_create()

            deposit_contracts = DepositContract.objects\
                .filter(
                    is_ended=False,
                    starts_at__lte=bank_settings.curr_bank_day,
                    ends_at__gte=bank_settings.curr_bank_day
                )\
                .prefetch_related(
                    'deposit_type',
                    'main_bank_account',
                    'deposit_bank_account',
                    'special_bank_account'
                )
            for deposit_contract in deposit_contracts:
                # Withdraw deposit if today is the last day of deposit
                if (bank_settings.curr_bank_day == deposit_contract.ends_at) and (not deposit_contract.is_ended):
                    deposit_withdraw(deposit_contract)
                    deposit_contract.is_ended = True
                    deposit_contract.save()

                # Deposit interest accrual if today is deposit day (started, but not ended)
                elif (deposit_contract.starts_at <= bank_settings.curr_bank_day) and \
                        (bank_settings.curr_bank_day < deposit_contract.ends_at) and \
                        (not deposit_contract.is_ended):
                    deposit_interest_accrual(deposit_contract)
                    deposit_contract.save()

            # Future: credit funcs
            # ...

            # Update current date in bank settings to +1
            bank_settings.curr_bank_day = F('curr_bank_day') + timedelta(days=1)
            bank_settings.save()

        return Response({'success': 'Bank\'s day has been closed successfully!'})
