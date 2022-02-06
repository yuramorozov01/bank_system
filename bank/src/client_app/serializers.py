from client_app.models import Client
from rest_framework import serializers


class ClientCreateSerializer(serializers.ModelSerializer):
    '''Serializer for creating and updating clients'''

    class Meta:
        model = Client
        fields = '__all__'

    def validate(self, data):
        birthday = data.get('birthday')
        passport_issued_at = data.get('passport_issued_at')
        if (birthday is not None) and (passport_issued_at is not None):

            # Check if birthday date is earlier than passport issue data
            if birthday > passport_issued_at:
                raise serializers.ValidationError({
                    'birthday': 'Birthday can\'t be after passport issue date!',
                    'passport_issued_at': 'Passport issue date can\'t be before birthday!',
                })
        return data


class ClientDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified client
    This serializer provides detailed information about client.
    '''

    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ['id', 'last_name', 'first_name', 'patronymic', 'birthday', 'birthday_place', 'sex',
                            'passport_series', 'passport_number', 'passport_issued_by', 'passport_issued_at',
                            'id_number', 'city', 'address', 'home_number', 'phone_number', 'email', 'job_place',
                            'job_position', 'register_city', 'register_address', 'family_status', 'citizen',
                            'disability', 'pensioner', 'monthly_salary', 'army']


class ClientShortDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified client
    This serializer provides short information about client.
    '''

    sex = serializers.CharField(source='get_sex_display')

    class Meta:
        model = Client
        fields = ['id', 'last_name', 'first_name', 'patronymic', 'birthday', 'sex', 'passport_series',
                  'passport_number', 'id_number']
        read_only_fields = ['id', 'last_name', 'first_name', 'patronymic', 'birthday', 'sex', 'passport_series',
                            'passport_number', 'id_number']


class ClientUpdateSerializer(serializers.ModelSerializer):
    '''Serializer for updating a specified client.
    '''

    class Meta:
        model = Client
        fields = '__all__'
