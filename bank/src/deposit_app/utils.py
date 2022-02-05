def generate_bank_account_number(client, amount_of_bank_accounts):
    return '{0}{1}{2}{3}'.format(3014, str(client.id).zfill(5), str(amount_of_bank_accounts).zfill(3), 1)
