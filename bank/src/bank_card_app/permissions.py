from rest_framework import permissions


class IsAuthenticatedBankCard(permissions.BasePermission):
    '''
    Allows access only to authenticated bank card.
    '''

    message = 'Bank card is not authenticated.'

    def has_permission(self, request, view):
        return bool(request.bank_card is not None)


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


class IsAuthenticatedBankCardOrCanViewBankCard(permissions.BasePermission):
    '''
    Allow access only to authenticated bank card or user who can view bank card
    '''

    message = 'You don\'t have permissions to view the bank card.'

    def has_permission(self, request, view):
        is_authenticated_bank_card_permission = IsAuthenticatedBankCard()
        can_view_bank_card_permission = CanViewBankCard()
        is_authenticated = permissions.IsAuthenticated()
        return bool(is_authenticated_bank_card_permission.has_permission(request, view) or
                    (can_view_bank_card_permission.has_permission(request, view) and
                     is_authenticated.has_permission(request, view)))
