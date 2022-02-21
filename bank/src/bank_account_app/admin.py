from bank_account_app.models import BankAccount
from django.contrib import admin
from base_app.utils import add_permissions_to_group

admin.site.register(BankAccount)

permissions_to_add = [
    {
        'group_name': 'bank_staff',
        'content_type_model': BankAccount,
        'permissions': ['view_bankaccount', 'change_bankaccount'],
    },
]

add_permissions_to_group(permissions_to_add)
