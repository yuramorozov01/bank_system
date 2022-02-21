from rest_framework import permissions


class CanAddCreditType(permissions.BasePermission):
    '''Permission to check if current user has permission to add credit types.'''

    message = 'You don\'t have permissions to add a new credit type.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('credit_app.add_credittype'))


class CanChangeCreditType(permissions.BasePermission):
    '''Permission to check if current user has permission to change credit types.'''

    message = 'You don\'t have permissions to change the credit type.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('credit_app.change_credittype'))


class CanDeleteCreditType(permissions.BasePermission):
    '''Permission to check if current user has permission to delete credit types.'''

    message = 'You don\'t have permissions to delete the credit type.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('credit_app.delete_credittype'))


class CanViewCreditType(permissions.BasePermission):
    '''Permission to check if current user has permission to view credit types.'''

    message = 'You don\'t have permissions to view the credit type.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('credit_app.view_credittype'))


class CanAddCreditContract(permissions.BasePermission):
    '''Permission to check if current user has permission to add credit contracts.'''

    message = 'You don\'t have permissions to add a new credit contract.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('credit_app.add_creditcontract'))


class CanChangeCreditContract(permissions.BasePermission):
    '''Permission to check if current user has permission to change credit contracts.'''

    message = 'You don\'t have permissions to change the credit contract.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('credit_app.change_creditcontract'))


class CanDeleteCreditContract(permissions.BasePermission):
    '''Permission to check if current user has permission to delete credit contracts.'''

    message = 'You don\'t have permissions to delete the credit contract.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('credit_app.delete_creditcontract'))


class CanViewCreditContract(permissions.BasePermission):
    '''Permission to check if current user has permission to view credit contracts.'''

    message = 'You don\'t have permissions to view the credit contract.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('credit_app.view_creditcontract'))
