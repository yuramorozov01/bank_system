from client_app.models import Client
from django.contrib import admin
from base_app.utils import add_permissions_to_group

admin.site.register(Client)

permissions_to_add = [
    {
        'group_name': 'bank_staff',
        'content_type_model': Client,
        'permissions': ['add_client', 'change_client', 'delete_client', 'view_client'],
    },
]

add_permissions_to_group(permissions_to_add)
