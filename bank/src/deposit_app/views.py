from rest_framework import permissions, serializers, viewsets

from deposit_app.models import DepositType, DepositContract
from bank_account_app.models import BankAccount
from client_app.models import Client
from deposit_app.permissions import (IsUserManagerAddDepositType,
                                    IsUserManagerChangeDepositType,
                                    IsUserManagerDeleteDepositType,
                                    IsUserManagerViewDepositType,
                                    IsUserManagerAddDepositContract,
                                    IsUserManagerChangeDepositContract,
                                    IsUserManagerDeleteDepositContract,
                                    IsUserManagerViewDepositContract)
from deposit_app.serializers import (DepositTypeCreateSerializer,
                                    DepositTypeDetailsSerializer,
                                    DepositTypeShortDetailsSerializer,
                                    DepositContractCreateSerializer,
                                    DepositContractDetailsSerializer,
                                    DepositContractShortDetailsSerializer)
from deposit_app.utils import generate_bank_account_number
from bank_account_app.choices import BankAccountActivityTypeChoices, BankAccountTypeChoices


class DepositTypeViewSet(viewsets.ModelViewSet):
    '''
    create:
        Create a new deposit type.
    destroy:
        Delete a deposit type.
    retrieve:
        Get the specified deposit type.
    list:
        Get a list of all deposit types.
    update:
        Update a deposit type.
    partial_update:
        Update a deposit type.
    '''

    def get_queryset(self):
        querysets_dict = {
            'create': DepositType.objects.all(),
            'destroy': DepositType.objects.all(),
            'retrieve': DepositType.objects.all(),
            'list': DepositType.objects.all(),
            'update': DepositType.objects.all(),
            'partial_update': DepositType.objects.all(),
        }
        queryset = querysets_dict.get(self.action)
        return queryset.distinct()

    def get_serializer_class(self):
        serializers_dict = {
            'create': DepositTypeCreateSerializer,
            'retrieve': DepositTypeDetailsSerializer,
            'list': DepositTypeShortDetailsSerializer,
            'update': DepositTypeCreateSerializer,
            'partial_update': DepositTypeCreateSerializer,
        }
        serializer_class = serializers_dict.get(self.action)
        return serializer_class

    def get_permissions(self):
        base_permissions = [permissions.IsAuthenticated, IsUserManagerViewDepositType]
        permissions_dict = {
            'create': [IsUserManagerAddDepositType],
            'destroy': [IsUserManagerDeleteDepositType],
            'retrieve': [],
            'list': [],
            'update': [IsUserManagerChangeDepositType],
            'partial_update': [IsUserManagerChangeDepositType],
        }
        base_permissions += permissions_dict.get(self.action, [])
        return [permission() for permission in base_permissions]


class DepositContractViewSet(viewsets.ModelViewSet):
    '''
    create:
        Create a new deposit contract.
    destroy:
        Delete a deposit contract.
    retrieve:
        Get the specified deposit contract.
    list:
        Get a list of all deposit contracts.
    update:
        Update a deposit contract.
    partial_update:
        Update a deposit contract.
    '''

    def get_queryset(self):
        querysets_dict = {
            'create': DepositContract.objects.all(),
            'destroy': DepositContract.objects.all(),
            'retrieve': DepositContract.objects.all(),
            'list': DepositContract.objects.all(),
            'update': DepositContract.objects.all(),
            'partial_update': DepositContract.objects.all(),
        }
        queryset = querysets_dict.get(self.action)
        return queryset.distinct()

    def get_serializer_class(self):
        serializers_dict = {
            'create': DepositContractCreateSerializer,
            'retrieve': DepositContractDetailsSerializer,
            'list': DepositContractShortDetailsSerializer,
            'update': DepositContractCreateSerializer,
            'partial_update': DepositContractCreateSerializer,
        }
        serializer_class = serializers_dict.get(self.action)
        return serializer_class

    def get_permissions(self):
        base_permissions = [permissions.IsAuthenticated, IsUserManagerViewDepositContract]
        permissions_dict = {
            'create': [IsUserManagerAddDepositContract],
            'destroy': [IsUserManagerDeleteDepositContract],
            'retrieve': [],
            'list': [],
            'update': [IsUserManagerChangeDepositContract],
            'partial_update': [IsUserManagerChangeDepositContract],
        }
        base_permissions += permissions_dict.get(self.action, [])
        return [permission() for permission in base_permissions]

    def perform_create(self, serializer):
        try:
            # ToDo:
            # 1. Top up balance to client's main bank account (pseudo)
            # 2. Creating main bank account only if client has not any main bank accounts
            # 3. With creating deposit contract transfer specified ...
            # ... deposit amount from main bank account to special fund.

            client = Client.objects.get(pk=self.request.POST.get('client'))
            amount_of_bank_accounts = BankAccount.objects.filter(client=client).count()

            new_main_bank_account_number = generate_bank_account_number(client, amount_of_bank_accounts)
            new_main_bank_account = BankAccount(
                number=new_main_bank_account_number,
                activity_type=BankAccountActivityTypeChoices.ACTIVE,
                bank_account_type=BankAccountTypeChoices.MAIN,
                balance=0,
                client=client
            )

            new_deposit_bank_account_number = generate_bank_account_number(client, amount_of_bank_accounts + 1)
            new_deposit_bank_account = BankAccount(
                number=new_deposit_bank_account_number,
                activity_type=BankAccountActivityTypeChoices.ACTIVE,
                bank_account_type=BankAccountTypeChoices.DEPOSIT,
                balance=0,
                client=client
            )
            new_main_bank_account.save()
            new_deposit_bank_account.save()
            serializer.save(main_bank_account=new_main_bank_account, deposit_bank_account=new_deposit_bank_account)
        except Client.DoesNotExist:
            raise serializers.ValidationError({
                'client': 'Specify client!',
            })
