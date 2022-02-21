from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


def add_permissions_to_group(permissions_to_add):
    '''

    :param permissions_to_add:
        List of dicts:
            group_name: str
            content_type_model: object
            permissions: list of str
    :return:
    '''

    for permission_info in permissions_to_add:
        group_name = permission_info['group_name']
        content_type_model = permission_info['content_type_model']
        permissions = permission_info['permissions']

        group, created = Group.objects.get_or_create(name=group_name)
        content_type = ContentType.objects.get_for_model(content_type_model)

        for permission in permissions:
            new_permission = Permission.objects.get(codename=permission, content_type=content_type)
            group.permissions.add(new_permission)
