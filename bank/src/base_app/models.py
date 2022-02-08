from decouple import config
from django.db import models


class BankSettings(models.Model):
    '''Bank settings model.
    Detailed information about bank settings.
    '''

    SETTINGS_NAME_CHOICES = [
        (config('DJANGO_SETTINGS_MODULE', default='bank.settings'),
         config('DJANGO_SETTINGS_MODULE', default='bank.settings')),
    ]
    settings_name = models.CharField(
        'Settings name',
        max_length=128,
        default=config('DJANGO_SETTINGS_MODULE', default='bank.settings'),
        choices=SETTINGS_NAME_CHOICES,
        primary_key=True
    )
    curr_bank_day = models.DateField('Current bank day', auto_now_add=True)

    class Meta:
        verbose_name = 'Bank settings'
        verbose_name_plural = 'Bank settings'

    def __str__(self):
        return f'{self.curr_bank_day}'
