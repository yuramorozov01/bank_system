from rest_framework import permissions


class CanViewBankSettings(permissions.BasePermission):
    '''Permission to check if current user has permission to view bank settings.'''

    message = 'You don\'t have permissions to view bank settings.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('base_app.view_banksettings'))
