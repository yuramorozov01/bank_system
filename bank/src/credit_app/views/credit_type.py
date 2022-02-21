from credit_app.models import CreditType
from credit_app.permissions import (CanAddCreditType, CanChangeCreditType,
                                    CanDeleteCreditType, CanViewCreditType)
from credit_app.serializers import (CreditTypeCreateSerializer,
                                    CreditTypeDetailsSerializer,
                                    CreditTypeShortDetailsSerializer)
from django.db.models.deletion import RestrictedError
from rest_framework import permissions, validators, viewsets


class CreditTypeViewSet(viewsets.ModelViewSet):
    '''
    create:
        Create a new credit type.
    destroy:
        Delete a credit type.
    retrieve:
        Get the specified credit type.
    list:
        Get a list of all credit types.
    update:
        Update a credit type.
    partial_update:
        Update a credit type.
    '''

    def get_queryset(self):
        querysets_dict = {
            'create': CreditType.objects.all(),
            'destroy': CreditType.objects.all(),
            'retrieve': CreditType.objects.all(),
            'list': CreditType.objects.all(),
            'update': CreditType.objects.all(),
            'partial_update': CreditType.objects.all(),
        }
        queryset = querysets_dict.get(self.action)
        return queryset.distinct()

    def get_serializer_class(self):
        serializers_dict = {
            'create': CreditTypeCreateSerializer,
            'retrieve': CreditTypeDetailsSerializer,
            'list': CreditTypeShortDetailsSerializer,
            'update': CreditTypeCreateSerializer,
            'partial_update': CreditTypeCreateSerializer,
        }
        serializer_class = serializers_dict.get(self.action)
        return serializer_class

    def get_permissions(self):
        base_permissions = [permissions.IsAuthenticated, CanViewCreditType]
        permissions_dict = {
            'create': [CanAddCreditType],
            'destroy': [CanDeleteCreditType],
            'retrieve': [],
            'list': [],
            'update': [CanChangeCreditType],
            'partial_update': [CanChangeCreditType],
        }
        base_permissions += permissions_dict.get(self.action, [])
        return [permission() for permission in base_permissions]

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except RestrictedError:
            raise validators.ValidationError({
                'credit_type': 'Cannot delete this credit type, because there are some credit contracts,'
                               ' that uses this type',
            })
