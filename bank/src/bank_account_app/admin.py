from bank_account_app.models import BankAccount
from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

admin.site.register(BankAccount)

bank_staff_group, created = Group.objects.get_or_create(name='bank_staff')

content_type = ContentType.objects.get_for_model(BankAccount)

view_bank_account_permission = Permission.objects.get(codename='view_bankaccount', content_type=content_type)
bank_staff_group.permissions.add(view_bank_account_permission)
