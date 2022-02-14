from credit_app.models import CreditContract, CreditType
from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

admin.site.register(CreditType)
admin.site.register(CreditContract)

bank_staff_group, created = Group.objects.get_or_create(name='bank_staff')

content_type = ContentType.objects.get_for_model(CreditType)

add_credit_type_permission = Permission.objects.get(codename='add_credittype', content_type=content_type)
bank_staff_group.permissions.add(add_credit_type_permission)

change_credit_type_permission = Permission.objects.get(codename='change_credittype', content_type=content_type)
bank_staff_group.permissions.add(change_credit_type_permission)

delete_credit_type_permission = Permission.objects.get(codename='delete_credittype', content_type=content_type)
bank_staff_group.permissions.add(delete_credit_type_permission)

view_credit_type_permission = Permission.objects.get(codename='view_credittype', content_type=content_type)
bank_staff_group.permissions.add(view_credit_type_permission)


content_type = ContentType.objects.get_for_model(CreditContract)

add_credit_contract_permission = Permission.objects.get(
    codename='add_creditcontract',
    content_type=content_type
)
bank_staff_group.permissions.add(add_credit_contract_permission)

change_credit_contract_permission = Permission.objects.get(
    codename='change_creditcontract',
    content_type=content_type
)
bank_staff_group.permissions.add(change_credit_contract_permission)

delete_credit_contract_permission = Permission.objects.get(
    codename='delete_creditcontract',
    content_type=content_type
)
bank_staff_group.permissions.add(delete_credit_contract_permission)

view_credit_contract_permission = Permission.objects.get(
    codename='view_creditcontract',
    content_type=content_type
)
bank_staff_group.permissions.add(view_credit_contract_permission)
