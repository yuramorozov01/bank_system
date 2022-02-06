from deposit_app.models import DepositContract, DepositType
from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

admin.site.register(DepositType)
admin.site.register(DepositContract)

bank_staff_group, created = Group.objects.get_or_create(name='bank_staff')

content_type = ContentType.objects.get_for_model(DepositType)

add_deposit_type_permission = Permission.objects.get(codename='add_deposittype', content_type=content_type)
bank_staff_group.permissions.add(add_deposit_type_permission)

change_deposit_type_permission = Permission.objects.get(codename='change_deposittype', content_type=content_type)
bank_staff_group.permissions.add(change_deposit_type_permission)

delete_deposit_type_permission = Permission.objects.get(codename='delete_deposittype', content_type=content_type)
bank_staff_group.permissions.add(delete_deposit_type_permission)

view_deposit_type_permission = Permission.objects.get(codename='view_deposittype', content_type=content_type)
bank_staff_group.permissions.add(view_deposit_type_permission)


content_type = ContentType.objects.get_for_model(DepositContract)

add_deposit_contract_permission = Permission.objects.get(
    codename='add_depositcontract',
    content_type=content_type
)
bank_staff_group.permissions.add(add_deposit_contract_permission)

change_deposit_contract_permission = Permission.objects.get(
    codename='change_depositcontract',
    content_type=content_type
)
bank_staff_group.permissions.add(change_deposit_contract_permission)

delete_deposit_contract_permission = Permission.objects.get(
    codename='delete_depositcontract',
    content_type=content_type
)
bank_staff_group.permissions.add(delete_deposit_contract_permission)

view_deposit_contract_permission = Permission.objects.get(
    codename='view_depositcontract',
    content_type=content_type
)
bank_staff_group.permissions.add(view_deposit_contract_permission)
