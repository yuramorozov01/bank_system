from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from client_app.models import Client

admin.site.register(Client)

bank_staff_group, created = Group.objects.get_or_create(name='bank_staff')
content_type = ContentType.objects.get_for_model(Client)

add_client_permission = Permission.objects.get(codename='add_client', content_type=content_type)
bank_staff_group.permissions.add(add_client_permission)

change_client_permission = Permission.objects.get(codename='change_client', content_type=content_type)
bank_staff_group.permissions.add(change_client_permission)

delete_client_permission = Permission.objects.get(codename='delete_client', content_type=content_type)
bank_staff_group.permissions.add(delete_client_permission)

view_client_permission = Permission.objects.get(codename='view_client', content_type=content_type)
bank_staff_group.permissions.add(view_client_permission)
