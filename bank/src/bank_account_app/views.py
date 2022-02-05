from rest_framework import permissions, serializers, viewsets, mixins
from bank_account_app.models import BankAccount
from bank_account_app.permissions import IsUserManagerViewBankAccount

from bank_account_app.serializers import (BankAccountDetailsSerializer,
                                          BankAccountShortDetailsSerializer)


class BankAccountViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
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
        }
        queryset = querysets_dict.get(self.action)
        return queryset.distinct()

    def get_serializer_class(self):
        serializers_dict = {
            'retrieve': BankAccountDetailsSerializer,
            'list': BankAccountShortDetailsSerializer,
        }
        serializer_class = serializers_dict.get(self.action)
        return serializer_class

    def get_permissions(self):
        base_permissions = [permissions.IsAuthenticated, IsUserManagerViewBankAccount]
        permissions_dict = {
            'retrieve': [],
            'list': [],
        }
        base_permissions += permissions_dict.get(self.action, [])
        return [permission() for permission in base_permissions]
