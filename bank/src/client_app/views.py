from bank_account_app.choices import (BankAccountActivityTypeChoices,
                                      BankAccountTypeChoices)
from bank_account_app.models import BankAccount
from bank_account_app.utils import generate_bank_account_number
from client_app.models import Client
from client_app.permissions import (CanAddClient, CanChangeClient,
                                    CanDeleteClient, CanViewClient)
from client_app.serializers import (ClientCreateSerializer,
                                    ClientDetailsSerializer,
                                    ClientShortDetailsSerializer)
from django.db import transaction
from rest_framework import permissions, viewsets


class ClientViewSet(viewsets.ModelViewSet):
    '''
    create:
        Create a new client.
    destroy:
        Delete a client.
    retrieve:
        Get the specified client.
    list:
        Get a list of all clients.
    update:
        Update a client.
    partial_update:
        Update a client.
    '''

    def get_queryset(self):
        querysets_dict = {
            'create': Client.objects.all(),
            'destroy': Client.objects.all(),
            'retrieve': Client.objects.all(),
            'list': Client.objects.all(),
            'update': Client.objects.all(),
            'partial_update': Client.objects.all(),
        }
        queryset = querysets_dict.get(self.action)
        return queryset.distinct()

    def get_serializer_class(self):
        serializers_dict = {
            'create': ClientCreateSerializer,
            'retrieve': ClientDetailsSerializer,
            'list': ClientShortDetailsSerializer,
            'update': ClientCreateSerializer,
            'partial_update': ClientCreateSerializer,
        }
        serializer_class = serializers_dict.get(self.action)
        return serializer_class

    def get_permissions(self):
        base_permissions = [permissions.IsAuthenticated, CanViewClient]
        permissions_dict = {
            'create': [CanAddClient],
            'destroy': [CanDeleteClient],
            'retrieve': [],
            'list': [],
            'update': [CanChangeClient],
            'partial_update': [CanChangeClient],
        }
        base_permissions += permissions_dict.get(self.action, [])
        return [permission() for permission in base_permissions]

    def perform_create(self, serializer):
        # Automatically create new main bank account after creating client
        with transaction.atomic():
            client = serializer.save()
            new_main_bank_account_number = generate_bank_account_number(client, 0)
            new_main_bank_account = BankAccount(
                number=new_main_bank_account_number,
                activity_type=BankAccountActivityTypeChoices.ACTIVE,
                bank_account_type=BankAccountTypeChoices.MAIN,
                balance=0,
                client=client
            )
            new_main_bank_account.save()
