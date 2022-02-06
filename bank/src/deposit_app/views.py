from bank_account_app.choices import (BankAccountActivityTypeChoices,
                                      BankAccountTypeChoices)
from bank_account_app.models import BankAccount
from bank_account_app.utils import (generate_bank_account_number,
                                    generate_special_fund_bank_account_number,
                                    transfer_money)
from client_app.models import Client
from deposit_app.models import DepositContract, DepositType
from deposit_app.permissions import (IsUserManagerAddDepositContract,
                                     IsUserManagerAddDepositType,
                                     IsUserManagerChangeDepositContract,
                                     IsUserManagerChangeDepositType,
                                     IsUserManagerDeleteDepositContract,
                                     IsUserManagerDeleteDepositType,
                                     IsUserManagerViewDepositContract,
                                     IsUserManagerViewDepositType)
from deposit_app.serializers import (DepositContractCreateSerializer,
                                     DepositContractDetailsSerializer,
                                     DepositContractShortDetailsSerializer,
                                     DepositTypeCreateSerializer,
                                     DepositTypeDetailsSerializer,
                                     DepositTypeShortDetailsSerializer)
from django.db import transaction
from rest_framework import permissions, validators, viewsets


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
            client = Client.objects.get(pk=self.request.POST.get('client'))
            with transaction.atomic():

                # Create new main bank account if it doesn't exist
                amount_of_bank_accounts = BankAccount.objects.filter(client=client).count()

                new_main_bank_account_number = generate_bank_account_number(client, amount_of_bank_accounts)
                new_main_bank_account, created = BankAccount.objects.get_or_create(
                    bank_account_type=BankAccountTypeChoices.MAIN,
                    client=client,
                    defaults={
                        'number': new_main_bank_account_number,
                        'activity_type': BankAccountActivityTypeChoices.ACTIVE,
                        'bank_account_type': BankAccountTypeChoices.MAIN,
                        'balance': 0,
                        'client': client,
                    }
                )

                # Create new deposit bank account
                new_deposit_bank_account_number = generate_bank_account_number(client, amount_of_bank_accounts + 1)
                new_deposit_bank_account = BankAccount.objects.create(
                    number=new_deposit_bank_account_number,
                    activity_type=BankAccountActivityTypeChoices.ACTIVE,
                    bank_account_type=BankAccountTypeChoices.DEPOSIT,
                    balance=0,
                    client=client
                )

                # Validate in serializer new data with bank accounts
                context_data = {
                    'main_bank_account': new_main_bank_account,
                    'deposit_bank_account': new_deposit_bank_account,
                }
                serializer = DepositContractCreateSerializer(data=self.request.POST, context=context_data)
                serializer.is_valid(raise_exception=True)

                # Create deposit contract
                deposit_contract = serializer.save(
                    main_bank_account=new_main_bank_account,
                    deposit_bank_account=new_deposit_bank_account
                )

                # Create special fund bank account if it doesn't exist
                amount_of_special_funds = BankAccount.objects \
                    .filter(
                        bank_account_type=BankAccountTypeChoices.SPECIAL
                    ).count()

                special_fund_bank_account_number = generate_special_fund_bank_account_number(amount_of_special_funds)
                special_fund_bank_account, created = BankAccount.objects.get_or_create(
                    bank_account_type=BankAccountTypeChoices.SPECIAL,
                    client=None,
                    defaults={
                        'number': special_fund_bank_account_number,
                        'activity_type': BankAccountActivityTypeChoices.PASSIVE,
                        'bank_account_type': BankAccountTypeChoices.SPECIAL,
                        'balance': 100_000_000_000,
                        'client': None,
                    }
                )

                # Transfer deposited money from main bank account to the special fund
                transfer_money(new_main_bank_account, special_fund_bank_account, deposit_contract.deposit_amount)
                new_main_bank_account.save()
                special_fund_bank_account.save()

        except Client.DoesNotExist:
            raise validators.ValidationError({
                'client': 'Specify client!',
            })
