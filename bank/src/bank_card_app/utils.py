from django.contrib.auth.hashers import ScryptPasswordHasher
from random import randrange


def generate_bank_card_number(bank_account):
    amount_of_bank_cards = bank_account.bank_cards.count()
    return '{0}{1}'.format(bank_account.number, str(amount_of_bank_cards).zfill(3))


def hash_pin_code(pin):
    pin_str = str(pin).zfill(3)
    hasher = ScryptPasswordHasher()
    hashed_pin = hasher.encode(pin_str, hasher.salt())
    return hashed_pin
