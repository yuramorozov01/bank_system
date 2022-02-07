from bank_account_app.utils import transfer_money
from bank_account_app.choices import BankAccountActivityTypeChoices
from decimal import Decimal


def deposit_withdraw(deposit_contract):
    transfer_money(
        deposit_contract.deposit_bank_account,
        deposit_contract.main_bank_account,
        deposit_contract.deposit_bank_account.balance
    )
    transfer_money(
        deposit_contract.special_bank_account,
        deposit_contract.main_bank_account,
        deposit_contract.deposit_amount
    )
    deposit_contract.deposit_bank_account.activity_type = BankAccountActivityTypeChoices.PASSIVE


def deposit_interest_accrual(deposit_contract):
    total_balance = deposit_contract.deposit_bank_account.balance + deposit_contract.deposit_amount
    percent = deposit_contract.deposit_type.percent
    term = deposit_contract.deposit_type.deposit_term
    transfer_amount = total_balance * (Decimal(percent) / 100) / term
    transfer_money(
        deposit_contract.special_bank_account,
        deposit_contract.deposit_bank_account,
        transfer_amount
    )
