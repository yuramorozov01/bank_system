from bank_account_app.choices import (BankAccountActivityTypeChoices,
                                      BankAccountTypeChoices)
from bank_account_app.models import BankAccount
from bank_account_app.utils import (generate_bank_account_number,
                                    get_or_create_main_bank_account,
                                    get_or_create_special_fund_bank_account,
                                    transfer_money)
from bank_card_app.models import BankCard
from bank_card_app.utils import generate_bank_card_number, hash_pin_code
from base_app.mixins import CustomCreateModelMixin
from base_app.models import BankSettings
from client_app.models import Client
from credit_app.models import CreditContract
from credit_app.permissions import (CanAddCreditContract,
                                    CanChangeCreditContract,
                                    CanViewCreditContract)
from credit_app.serializers import (CreditContractCreateSerializer,
                                    CreditContractDetailsSerializer,
                                    CreditContractShortDetailsSerializer)
from credit_app.utils import credit_payoff
from django.db import transaction
from rest_framework import mixins, permissions, validators, viewsets
from rest_framework.decorators import action


class CreditContractViewSet(CustomCreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    '''
    create:
        Create a new credit contract.
        Have to be specified PIN for credit bank card as POST param `pin`.
    retrieve:
        Get the specified credit contract.
    list:
        Get a list of all credit contracts.
    pay_off:
        Finish credit contract by paying all debts.
    '''

    def get_queryset(self):
        querysets_dict = {
            'create': CreditContract.objects.all(),
            'retrieve': CreditContract.objects.all(),
            'list': CreditContract.objects.all(),
            'pay_off': CreditContract.objects.all(),
        }
        queryset = querysets_dict.get(self.action)
        return queryset.distinct()

    def get_serializer_class(self):
        serializers_dict = {
            'create': CreditContractCreateSerializer,
            'retrieve': CreditContractDetailsSerializer,
            'list': CreditContractShortDetailsSerializer,
            'pay_off': CreditContractDetailsSerializer,
        }
        serializer_class = serializers_dict.get(self.action)
        return serializer_class

    def get_permissions(self):
        base_permissions = [permissions.IsAuthenticated, CanViewCreditContract]
        permissions_dict = {
            'create': [CanAddCreditContract],
            'retrieve': [],
            'list': [],
            'pay_off': [CanChangeCreditContract]
        }
        base_permissions += permissions_dict.get(self.action, [])
        return [permission() for permission in base_permissions]

    def perform_create(self, serializer):
        try:
            client = Client.objects.get(pk=self.request.data.get('client'))
            with transaction.atomic():

                # Create new main bank account if it doesn't exist
                amount_of_bank_accounts, new_main_bank_account, created = get_or_create_main_bank_account(client)

                # Create new credit bank account

                # If new main bank account has been created, increment amount of user's bank accounts
                if created:
                    amount_of_bank_accounts += 1

                new_credit_bank_account_number = generate_bank_account_number(client, amount_of_bank_accounts)
                new_credit_bank_account = BankAccount.objects.create(
                    number=new_credit_bank_account_number,
                    activity_type=BankAccountActivityTypeChoices.ACTIVE,
                    bank_account_type=BankAccountTypeChoices.CREDIT,
                    balance=0,
                    client=client
                )

                # Create bank card for a credit bank account
                pin = self.request.POST.get('pin')
                if pin is None:
                    raise validators.ValidationError({
                        'pin': ['Specify PIN! (3 digits)'],
                    })
                else:
                    if len(pin) != 3:
                        raise validators.ValidationError({
                            'pin': ['Specify correct PIN! Only 3 digits!'],
                        })
                    try:
                        pin_int = int(pin)
                    except ValueError:
                        raise validators.ValidationError({
                            'pin': ['Specify correct PIN! Only 3 digits!'],
                        })
                new_bank_card = BankCard.objects.create(
                    number=generate_bank_card_number(new_credit_bank_account),
                    pin=hash_pin_code(pin),
                    bank_account=new_credit_bank_account,
                )

                # Validate in serializer new data with bank accounts
                context_data = {
                    'main_bank_account': new_main_bank_account,
                    'credit_bank_account': new_credit_bank_account,
                }
                serializer = type(serializer)(data=self.request.data, context=context_data)
                serializer.is_valid(raise_exception=True)

                # Create special fund bank account if it doesn't exist
                special_fund_bank_account = get_or_create_special_fund_bank_account()

                # Create credit contract
                credit_contract = serializer.save(
                    main_bank_account=new_main_bank_account,
                    credit_bank_account=new_credit_bank_account,
                    special_bank_account=special_fund_bank_account
                )

                # Change viewset serializer with serializer with additional arguments
                self.custom_serializer = serializer

                # Transfer credited money from main bank account to the special fund
                transfer_money(special_fund_bank_account, new_main_bank_account, credit_contract.credit_amount)
                special_fund_bank_account.save()
                new_main_bank_account.save()

        except Client.DoesNotExist:
            raise validators.ValidationError({
                'client': 'Specify client!',
            })

    @action(methods=['PUT', 'PATCH'], detail=True)
    def pay_off(self, request, pk=None):
        try:
            with transaction.atomic():
                credit_contract = self.get_queryset().filter(is_ended=False).get(pk=pk)
                bank_setting, _ = BankSettings.objects.get_or_create()
                credit_payoff(bank_setting, credit_contract)
            return self.retrieve(request, pk=pk)
        except CreditContract.DoesNotExist:
            raise validators.ValidationError({
                'credit_contract': 'Credit contract with specified id doesn\'t exists or had been ended!',
            })
