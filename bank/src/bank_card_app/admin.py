from bank_card_app.models import BankCard
from base_app.utils import add_permissions_to_group
from django.contrib import admin

admin.site.register(BankCard)

permissions_to_add = [
    {
        'group_name': 'bank_staff',
        'content_type_model': BankCard,
        'permissions': ['add_bankcard', 'delete_bankcard', 'view_bankcard'],
    },
]

add_permissions_to_group(permissions_to_add)
