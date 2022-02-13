from decimal import Decimal

from bank_account_app.choices import BankAccountActivityTypeChoices
from bank_account_app.utils import transfer_money


def deposit_withdraw(deposit_contract):
    deposit_bank_account = deposit_contract.deposit_bank_account
    main_bank_account = deposit_contract.main_bank_account

    transfer_money(
        deposit_bank_account,
        main_bank_account,
        deposit_bank_account.balance
    )

    deposit_bank_account.activity_type = BankAccountActivityTypeChoices.PASSIVE
    deposit_bank_account.save()
    deposit_bank_account.refresh_from_db()

    main_bank_account.save()
    main_bank_account.refresh_from_db()

    special_bank_account = deposit_contract.special_bank_account

    transfer_money(
        special_bank_account,
        main_bank_account,
        deposit_contract.deposit_amount
    )

    special_bank_account.save()
    special_bank_account.refresh_from_db()

    main_bank_account.save()
    main_bank_account.refresh_from_db()


def deposit_interest_accrual(deposit_contract):
    total_balance = deposit_contract.deposit_bank_account.balance + deposit_contract.deposit_amount
    percent = deposit_contract.deposit_type.percent
    term = deposit_contract.deposit_type.deposit_term
    transfer_amount = total_balance * (Decimal(percent) / 100) / term

    special_bank_account = deposit_contract.special_bank_account
    deposit_bank_account = deposit_contract.deposit_bank_account

    transfer_money(
        special_bank_account,
        deposit_bank_account,
        transfer_amount
    )

    special_bank_account.save()
    special_bank_account.refresh_from_db()

    deposit_bank_account.save()
    deposit_bank_account.refresh_from_db()
