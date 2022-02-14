from bank_account_app.choices import (BankAccountActivityTypeChoices,
                                      BankAccountTypeChoices)
from bank_account_app.models import BankAccount
from django.db.models import F


def generate_bank_account_number(client, amount_of_bank_accounts):
    return '{0}{1}{2}{3}'.format(3014, str(client.id).zfill(5), str(amount_of_bank_accounts).zfill(3), 1)


def generate_special_fund_bank_account_number(amount_of_bank_accounts):
    return '{0}{1}{2}'.format(7327, str(amount_of_bank_accounts).zfill(8), 1)


def get_or_create_main_bank_account(client):
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
    return amount_of_bank_accounts, new_main_bank_account, created


def get_or_create_special_fund_bank_account():
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
    return special_fund_bank_account


def transfer_money(src, dest, amount):
    src.balance = F('balance') - amount
    dest.balance = F('balance') + amount
