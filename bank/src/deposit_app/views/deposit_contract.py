from bank_account_app.choices import (BankAccountActivityTypeChoices,
                                      BankAccountTypeChoices)
from bank_account_app.models import BankAccount
from bank_account_app.utils import (generate_bank_account_number,
                                    get_or_create_main_bank_account,
                                    get_or_create_special_fund_bank_account,
                                    transfer_money)
from base_app.mixins import CustomCreateModelMixin
from client_app.models import Client
from deposit_app.models import DepositContract
from deposit_app.permissions import (IsUserManagerAddDepositContract,
                                     IsUserManagerChangeDepositContract,
                                     IsUserManagerViewDepositContract)
from deposit_app.serializers import (DepositContractCreateSerializer,
                                     DepositContractDetailsSerializer,
                                     DepositContractShortDetailsSerializer)
from deposit_app.utils import deposit_withdraw
from django.db import transaction
from rest_framework import mixins, permissions, validators, viewsets
from rest_framework.decorators import action


class DepositContractViewSet(CustomCreateModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    '''
    create:
        Create a new deposit contract.
    retrieve:
        Get the specified deposit contract.
    list:
        Get a list of all deposit contracts.
    '''

    def get_queryset(self):
        querysets_dict = {
            'create': DepositContract.objects.all(),
            'retrieve': DepositContract.objects.all(),
            'list': DepositContract.objects.all(),
            'revoke': DepositContract.objects.all(),
        }
        queryset = querysets_dict.get(self.action)
        return queryset.distinct()

    def get_serializer_class(self):
        serializers_dict = {
            'create': DepositContractCreateSerializer,
            'retrieve': DepositContractDetailsSerializer,
            'list': DepositContractShortDetailsSerializer,
            'revoke': DepositContractDetailsSerializer,
        }
        serializer_class = serializers_dict.get(self.action)
        return serializer_class

    def get_permissions(self):
        base_permissions = [permissions.IsAuthenticated, IsUserManagerViewDepositContract]
        permissions_dict = {
            'create': [IsUserManagerAddDepositContract],
            'retrieve': [],
            'list': [],
            'revoke': [IsUserManagerChangeDepositContract]
        }
        base_permissions += permissions_dict.get(self.action, [])
        return [permission() for permission in base_permissions]

    def perform_create(self, serializer):
        try:
            client = Client.objects.get(pk=self.request.data.get('client'))
            with transaction.atomic():

                # Create new main bank account if it doesn't exist
                amount_of_bank_accounts, new_main_bank_account, created = get_or_create_main_bank_account(client)

                # Create new deposit bank account

                # If new main bank account has been created, increment amount of user's bank accounts
                if created:
                    amount_of_bank_accounts += 1

                new_deposit_bank_account_number = generate_bank_account_number(client, amount_of_bank_accounts)
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
                serializer = type(serializer)(data=self.request.data, context=context_data)
                serializer.is_valid(raise_exception=True)

                # Create special fund bank account if it doesn't exist
                special_fund_bank_account = get_or_create_special_fund_bank_account()

                # Create deposit contract
                deposit_contract = serializer.save(
                    main_bank_account=new_main_bank_account,
                    deposit_bank_account=new_deposit_bank_account,
                    special_bank_account=special_fund_bank_account
                )

                # Change viewset serializer with serializer with additional arguments
                self.custom_serializer = serializer

                # Transfer deposited money from main bank account to the special fund
                transfer_money(new_main_bank_account, special_fund_bank_account, deposit_contract.deposit_amount)
                new_main_bank_account.save()
                special_fund_bank_account.save()

        except Client.DoesNotExist:
            raise validators.ValidationError({
                'client': 'Specify client!',
            })

    @action(methods=['PUT', 'PATCH'], detail=True)
    def revoke(self, request, pk=None):
        try:
            with transaction.atomic():
                deposit_contract = self.get_queryset().filter(is_ended=False).get(pk=pk)
                if deposit_contract.deposit_type.is_revocable:
                    deposit_withdraw(deposit_contract)
                else:
                    raise validators.ValidationError({
                        'deposit_contract': 'Deposit type of deposit contract is not revocable!',
                    })
            return self.retrieve(request, pk=pk)
        except DepositContract.DoesNotExist:
            raise validators.ValidationError({
                'deposit_contract': 'Deposit contract with specified id doesn\'t exists or had been ended!',
            })
