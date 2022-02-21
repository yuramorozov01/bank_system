from bank_card_app.models import BankCard
from bank_card_app.permissions import IsAuthenticatedBankCardOrCanViewBankCard
from bank_card_app.serializers import BankCardShortDetailsSerializer
from rest_framework import mixins, viewsets


class BankCardViewSet(mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    '''
    retrieve:
        Get the specified bank card.
    '''

    def get_queryset(self):
        querysets_dict = {
            'retrieve': BankCard.objects.all(),
        }
        queryset = querysets_dict.get(self.action)
        return queryset.distinct()

    def get_serializer_class(self):
        serializers_dict = {
            'retrieve': BankCardShortDetailsSerializer,
        }
        serializer_class = serializers_dict.get(self.action)
        return serializer_class

    def get_permissions(self):
        base_permissions = []
        permissions_dict = {
            'retrieve': [IsAuthenticatedBankCardOrCanViewBankCard],
        }
        base_permissions += permissions_dict.get(self.action, [])
        return [permission() for permission in base_permissions]
