from rest_framework import permissions


class CanAddBankCard(permissions.BasePermission):
    '''Permission to check if current user has permission to add bank cards.'''

    message = 'You don\'t have permissions to add the bank card.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('bank_card_app.add_bankcard'))


class CanDeleteBankCard(permissions.BasePermission):
    '''Permission to check if current user has permission to delete bank cards.'''

    message = 'You don\'t have permissions to delete the bank card.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('bank_card_app.delete_bankcard'))


class CanViewBankCard(permissions.BasePermission):
    '''Permission to check if current user has permission to view bank cards.'''

    message = 'You don\'t have permissions to view the bank card.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('bank_card_app.view_bankcard'))
