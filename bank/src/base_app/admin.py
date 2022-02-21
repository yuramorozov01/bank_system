from base_app.models import BankSettings
from base_app.utils import add_permissions_to_group
from django.contrib import admin

admin.site.register(BankSettings)

bank_settings, _ = BankSettings.objects.get_or_create()

permissions_to_add = [
    {
        'group_name': 'bank_staff',
        'content_type_model': BankSettings,
        'permissions': ['view_banksettings'],
    },
]

add_permissions_to_group(permissions_to_add)
