from datetime import timedelta

from bank_account_app.permissions import (CanChangeBankAccount,
                                          CanViewBankAccount)
from base_app.models import BankSettings
from base_app.permissions import CanViewBankSettings
from base_app.serializers import BankSettingsDetailsSerializer
from credit_app.utils import credit_daily_recount
from deposit_app.permissions import (CanChangeDepositContract,
                                     CanViewDepositContract,
                                     CanViewDepositType)
from deposit_app.utils import deposit_daily_recount
from django.db import transaction
from django.db.models import F
from rest_framework import permissions, viewsets
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
        base_permissions = [permissions.IsAuthenticated, CanViewBankSettings, CanViewBankAccount,
                            CanViewDepositType, CanViewDepositContract]
        permissions_dict = {
            'list': [],
            'close_day': [CanChangeBankAccount, CanChangeDepositContract],
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
            bank_settings, _ = BankSettings.objects.select_for_update().get_or_create()
            deposit_daily_recount(bank_settings)
            credit_daily_recount(bank_settings)

            # Update current date in bank settings to +1
            bank_settings.curr_bank_day = F('curr_bank_day') + timedelta(days=1)
            bank_settings.save()
            bank_settings.refresh_from_db()

        bank_settings, _ = self.get_queryset()
        serializer = self.get_serializer(bank_settings)
        return Response(serializer.data)
