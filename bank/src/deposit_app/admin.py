from base_app.utils import add_permissions_to_group
from deposit_app.models import DepositContract, DepositType
from django.contrib import admin

admin.site.register(DepositType)
admin.site.register(DepositContract)

permissions_to_add = [
    {
        'group_name': 'bank_staff',
        'content_type_model': DepositType,
        'permissions': ['add_deposittype', 'change_deposittype', 'delete_deposittype', 'view_deposittype'],
    },
    {
        'group_name': 'bank_staff',
        'content_type_model': DepositContract,
        'permissions': ['add_depositcontract', 'change_depositcontract',
                        'delete_depositcontract', 'view_depositcontract'],
    },
]

add_permissions_to_group(permissions_to_add)
