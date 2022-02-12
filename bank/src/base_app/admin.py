from base_app.models import BankSettings
from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

admin.site.register(BankSettings)

bank_settings, _ = BankSettings.objects.get_or_create()

bank_staff_group, _ = Group.objects.get_or_create(name='bank_staff')

content_type = ContentType.objects.get_for_model(BankSettings)

view_bank_settings_permission = Permission.objects.get(codename='view_banksettings', content_type=content_type)
bank_staff_group.permissions.add(view_bank_settings_permission)
