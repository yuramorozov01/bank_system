from django.db.models import F


def generate_bank_account_number(client, amount_of_bank_accounts):
    return '{0}{1}{2}{3}'.format(3014, str(client.id).zfill(5), str(amount_of_bank_accounts).zfill(3), 1)


def generate_special_fund_bank_account_number(amount_of_bank_accounts):
    return '{0}{1}{2}'.format(3014, str(amount_of_bank_accounts).zfill(8), 1)


def transfer_money(src, dest, amount):
    src.balance = F('balance') - amount
    dest.balance = F('balance') + amount
