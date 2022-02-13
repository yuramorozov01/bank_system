from datetime import timedelta

from base_app.permissions import IsUserManagerViewBankSettings
from base_app.serializers import BankSettingsDetailsSerializer
from bank_account_app.permissions import (IsUserManagerChangeBankAccount,
                                          IsUserManagerViewBankAccount)
from base_app.models import BankSettings
from deposit_app.models import DepositContract
from deposit_app.permissions import (IsUserManagerChangeDepositContract,
                                     IsUserManagerViewDepositContract,
                                     IsUserManagerViewDepositType)
from deposit_app.utils import deposit_interest_accrual, deposit_withdraw
from django.db import transaction
from django.db.models import F
from rest_framework import permissions, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response


class BankSettingsViewSet(viewsets.GenericViewSet):
    '''
    list:
        Get bank settings
    close_day:
        Update bank accounts balances (with deposits and credits programs)
    '''

    def get_queryset(self):
        querysets_dict = {
            'list': BankSettings.objects.get_or_create(),
            'close_day': BankSettings.objects.get_or_create(),
        }
        queryset = querysets_dict.get(self.action)
        return queryset

    def get_serializer_class(self):
        serializers_dict = {
            'list': BankSettingsDetailsSerializer,
            'close_day': BankSettingsDetailsSerializer,
        }
        serializer_class = serializers_dict.get(self.action)
        return serializer_class

    def get_permissions(self):
        base_permissions = [permissions.IsAuthenticated, IsUserManagerViewBankSettings, IsUserManagerViewBankAccount,
                            IsUserManagerViewDepositType, IsUserManagerViewDepositContract]
        permissions_dict = {
            'list': [],
            'close_day': [IsUserManagerChangeBankAccount, IsUserManagerChangeDepositContract],
        }
        base_permissions += permissions_dict.get(self.action, [])
        return [permission() for permission in base_permissions]

    def list(self, request, *args, **kwargs):
        bank_settings, _ = self.get_queryset()
        serializer = self.get_serializer(bank_settings)
        return Response(serializer.data)

    @action(methods=['PUT', 'PATCH'], detail=False)
    def close_day(self, request):
        with transaction.atomic():
            bank_settings, _ = self.get_queryset()

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
                # Deposit interest accrual if today is deposit day
                if (deposit_contract.starts_at <= bank_settings.curr_bank_day) and \
                        (bank_settings.curr_bank_day <= deposit_contract.ends_at) and \
                        (not deposit_contract.is_ended):
                    deposit_interest_accrual(deposit_contract)
                    deposit_contract.save()

                # Withdraw deposit if today is the last day of deposit
                if (bank_settings.curr_bank_day == deposit_contract.ends_at) and (not deposit_contract.is_ended):
                    deposit_withdraw(deposit_contract)
                    deposit_contract.is_ended = True
                    deposit_contract.save()

            # Future: credit funcs
            # ...

            # Update current date in bank settings to +1
            bank_settings.curr_bank_day = F('curr_bank_day') + timedelta(days=1)
            bank_settings.save()

        bank_settings, _ = self.get_queryset()
        serializer = self.get_serializer(bank_settings)
        return Response(serializer.data)
