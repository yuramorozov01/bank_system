from decimal import Decimal

from bank_account_app.choices import BankAccountActivityTypeChoices
from bank_account_app.utils import transfer_money
from base_app.models import BankSettings
from credit_app.models import CreditContract


def calc_debt_amount(bank_settings, credit_contract, pay_off=False):
    days_left = 1
    if pay_off:
        # Calculate number of days left until credit end date
        # +1 in `days_left` means including current day
        # days_left` will be not equal to 1 only if current operation is pay off
        days_left = (credit_contract.ends_at - bank_settings.curr_bank_day).days + 1

    # Calculate debt amount
    credit_amount = credit_contract.credit_amount
    percent = Decimal(credit_contract.credit_type.percent) / 100
    credit_term = credit_contract.credit_type.credit_term

    # Differential single debt amount
    # In case of payoff operation, debt amount will be calculated by ...
    # ... multiplying on left days (1 means last day) and addition with sum of credit
    debt_amount = ((credit_amount * percent) / credit_term) * days_left

    if pay_off:
        debt_amount += credit_amount

    # Annuity single debt amount
    # In case of payoff operation, debt amount will be calculated by ...
    # ... multiplying on left days (1 means last day)
    if credit_contract.credit_type.is_annuity_payment:
        debt_amount = (credit_amount * (1 + percent) / credit_term) * days_left

    return debt_amount


def make_credit_payment(bank_settings, credit_contract, pay_off=False):
    debt_amount = calc_debt_amount(bank_settings, credit_contract, pay_off=pay_off)

    # Transfer debt money from credit bank account to special fund bank account
    credit_bank_account = credit_contract.credit_bank_account
    special_bank_account = credit_contract.special_bank_account
    transfer_money(credit_bank_account, special_bank_account, debt_amount)

    if pay_off:
        credit_bank_account.activity_type = BankAccountActivityTypeChoices.PASSIVE

    credit_bank_account.save()
    credit_bank_account.refresh_from_db()

    special_bank_account.save()
    special_bank_account.refresh_from_db()


def credit_payoff(bank_settings, credit_contract):
    make_credit_payment(bank_settings, credit_contract, pay_off=True)
    credit_contract.is_ended = True
    credit_contract.save()
    credit_contract.refresh_from_db()


def credit_interest_payment(bank_settings, credit_contract):
    make_credit_payment(bank_settings, credit_contract, pay_off=False)
    credit_contract.save()
    credit_contract.refresh_from_db()


def credit_daily_recount(bank_settings):
    credit_contracts = CreditContract.objects\
        .select_for_update()\
        .filter(
            is_ended=False,
            starts_at__lte=bank_settings.curr_bank_day,
            ends_at__gte=bank_settings.curr_bank_day
        )\
        .prefetch_related(
            'credit_type',
            'main_bank_account',
            'credit_bank_account',
            'special_bank_account'
        )
    for credit_contract in credit_contracts:
        # Credit interest payment if today is credit day
        if (credit_contract.starts_at <= bank_settings.curr_bank_day) and \
           (bank_settings.curr_bank_day < credit_contract.ends_at):
            credit_interest_payment(bank_settings, credit_contract)

        # Pay off credit if today is the last day of credit
        elif bank_settings.curr_bank_day == credit_contract.ends_at:
            credit_payoff(bank_settings, credit_contract)
