from rest_framework import permissions


class IsUserManagerViewBankAccount(permissions.BasePermission):
    '''Permission to check if current user has permission to view bank accounts.'''

    message = 'You don\'t have permissions to view the bank account.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('bank_account_app.view_bankaccount'))


class IsUserManagerChangeBankAccount(permissions.BasePermission):
    '''Permission to check if current user has permission to change bank accounts.'''

    message = 'You don\'t have permissions to change the bank account.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('bank_account_app.change_bankaccount'))
