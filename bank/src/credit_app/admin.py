from base_app.utils import add_permissions_to_group
from credit_app.models import CreditContract, CreditType
from django.contrib import admin

admin.site.register(CreditType)
admin.site.register(CreditContract)

permissions_to_add = [
    {
        'group_name': 'bank_staff',
        'content_type_model': CreditType,
        'permissions': ['add_credittype', 'change_credittype', 'delete_credittype', 'view_credittype'],
    },
    {
        'group_name': 'bank_staff',
        'content_type_model': CreditContract,
        'permissions': ['add_creditcontract', 'change_creditcontract', 'delete_creditcontract', 'view_creditcontract'],
    },
]

add_permissions_to_group(permissions_to_add)
