from rest_framework import permissions


class CanAddClient(permissions.BasePermission):
    '''Permission to check if current user has permission to add clients.'''

    message = 'You don\'t have permissions to add a new client.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('client_app.add_client'))


class CanChangeClient(permissions.BasePermission):
    '''Permission to check if current user has permission to change clients.'''

    message = 'You don\'t have permissions to change the client.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('client_app.change_client'))


class CanDeleteClient(permissions.BasePermission):
    '''Permission to check if current user has permission to delete clients.'''

    message = 'You don\'t have permissions to delete the client.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('client_app.delete_client'))


class CanViewClient(permissions.BasePermission):
    '''Permission to check if current user has permission to view clients.'''

    message = 'You don\'t have permissions to view the client.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('client_app.view_client'))
