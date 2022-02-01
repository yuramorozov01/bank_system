from rest_framework import permissions, viewsets

from deposit_app.models import DepositType, DepositContract
from deposit_app.permissions import (IsUserManagerAddDepositType,
                                    IsUserManagerChangeDepositType,
                                    IsUserManagerDeleteDepositType,
                                    IsUserManagerViewDepositType,
                                    IsUserManagerAddDepositContract,
                                    IsUserManagerChangeDepositContract,
                                    IsUserManagerDeleteDepositContract,
                                    IsUserManagerViewDepositContract)
from deposit_app.serializers import (DepositTypeCreateSerializer,
                                    DepositTypeDetailsSerializer,
                                    DepositTypeShortDetailsSerializer,
                                    DepositContractCreateSerializer,
                                    DepositContractDetailsSerializer,
                                    DepositContractShortDetailsSerializer)


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


class DepositContractViewSet(viewsets.ModelViewSet):
    '''
    create:
        Create a new deposit contract.
    destroy:
        Delete a deposit contract.
    retrieve:
        Get the specified deposit contract.
    list:
        Get a list of all deposit contracts.
    update:
        Update a deposit contract.
    partial_update:
        Update a deposit contract.
    '''

    def get_queryset(self):
        querysets_dict = {
            'create': DepositContract.objects.all(),
            'destroy': DepositContract.objects.all(),
            'retrieve': DepositContract.objects.all(),
            'list': DepositContract.objects.all(),
            'update': DepositContract.objects.all(),
            'partial_update': DepositContract.objects.all(),
        }
        queryset = querysets_dict.get(self.action)
        return queryset.distinct()

    def get_serializer_class(self):
        serializers_dict = {
            'create': DepositContractCreateSerializer,
            'retrieve': DepositContractDetailsSerializer,
            'list': DepositContractShortDetailsSerializer,
            'update': DepositContractCreateSerializer,
            'partial_update': DepositContractCreateSerializer,
        }
        serializer_class = serializers_dict.get(self.action)
        return serializer_class

    def get_permissions(self):
        base_permissions = [permissions.IsAuthenticated, IsUserManagerViewDepositContract]
        permissions_dict = {
            'create': [IsUserManagerAddDepositContract],
            'destroy': [IsUserManagerDeleteDepositContract],
            'retrieve': [],
            'list': [],
            'update': [IsUserManagerChangeDepositContract],
            'partial_update': [IsUserManagerChangeDepositContract],
        }
        base_permissions += permissions_dict.get(self.action, [])
        return [permission() for permission in base_permissions]
