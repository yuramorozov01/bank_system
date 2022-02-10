from deposit_app.models import DepositType
from deposit_app.permissions import (IsUserManagerAddDepositType,
                                     IsUserManagerChangeDepositType,
                                     IsUserManagerDeleteDepositType,
                                     IsUserManagerViewDepositType)
from deposit_app.serializers import (DepositTypeCreateSerializer,
                                     DepositTypeDetailsSerializer,
                                     DepositTypeShortDetailsSerializer)
from django.db.models.deletion import RestrictedError
from rest_framework import permissions, validators, viewsets


class DepositTypeViewSet(viewsets.ModelViewSet):
    '''
    create:
        Create a new deposit type.
    destroy:
        Delete a deposit type.
    retrieve:
        Get the specified deposit type.
    list:
        Get a list of all deposit types.
    update:
        Update a deposit type.
    partial_update:
        Update a deposit type.
    '''

    def get_queryset(self):
        querysets_dict = {
            'create': DepositType.objects.all(),
            'destroy': DepositType.objects.all(),
            'retrieve': DepositType.objects.all(),
            'list': DepositType.objects.all(),
            'update': DepositType.objects.all(),
            'partial_update': DepositType.objects.all(),
        }
        queryset = querysets_dict.get(self.action)
        return queryset.distinct()

    def get_serializer_class(self):
        serializers_dict = {
            'create': DepositTypeCreateSerializer,
            'retrieve': DepositTypeDetailsSerializer,
            'list': DepositTypeShortDetailsSerializer,
            'update': DepositTypeCreateSerializer,
            'partial_update': DepositTypeCreateSerializer,
        }
        serializer_class = serializers_dict.get(self.action)
        return serializer_class

    def get_permissions(self):
        base_permissions = [permissions.IsAuthenticated, IsUserManagerViewDepositType]
        permissions_dict = {
            'create': [IsUserManagerAddDepositType],
            'destroy': [IsUserManagerDeleteDepositType],
            'retrieve': [],
            'list': [],
            'update': [IsUserManagerChangeDepositType],
            'partial_update': [IsUserManagerChangeDepositType],
        }
        base_permissions += permissions_dict.get(self.action, [])
        return [permission() for permission in base_permissions]

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except RestrictedError:
            raise validators.ValidationError({
                'deposit_type': 'Cannot delete this deposit type, because there are some deposit contracts,'
                                ' that uses this type',
            })
