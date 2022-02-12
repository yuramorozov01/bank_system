from base_app.models import BankSettings
from rest_framework import serializers


class BankSettingsDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a bank settings.
    This serializer provides detailed information about bank settings.
    '''

    class Meta:
        model = BankSettings
        fields = ['curr_bank_day']
        read_only_fields = ['curr_bank_day']
