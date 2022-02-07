from django.db import models

from decouple import config


class BankSettings(models.Model):
    '''Bank settings model.
    Detailed information about bank settings.
    '''

    settings_name = models.CharField(
        'Settings name',
        max_length=128,
        default=config('DJANGO_SETTINGS_MODULE', default='bank.settings'),
        primary_key=True
    )
    curr_bank_day = models.DateField('Current bank day', auto_now_add=True)

    class Meta:
        verbose_name = 'Bank settings'
        verbose_name_plural = 'Bank settings'

    def __str__(self):
        return f'{self.curr_bank_day}'
