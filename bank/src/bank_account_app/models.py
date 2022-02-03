from django.db import models
from django.core.validators import RegexValidator

from bank_account_app.choices import (BankAccountActivityTypeChoices, BankAccountTypeChoices)


class BankAccount(models.Model):
    '''Bank account model.
    Detailed information about bank accounts.
    '''

    number = models.CharField(
        'Name',
        max_length=13,
        unique=True,
        validators=[RegexValidator(
            regex='^[0-9]{13}$',
            message='Incorrect number'
        )]
    )
    activity_type = models.CharField('Activity type', choices=BankAccountActivityTypeChoices.choices, max_length=128)
    # bank_account_type = models.CharField('Type', choices=BankAccountTypeChoices.choices, max_length=128)
    balance = models.DecimalField(
        'Balance',
        max_digits=13,
        decimal_places=2
    )
    client = models.ForeignKey(
        'client_app.Client',
        verbose_name='Client',
        on_delete=models.RESTRICT,
        related_name='bank_accounts'
    )

    class Meta:
        ordering = ['number']
        verbose_name = 'Bank account'
        verbose_name_plural = 'Bank accounts'

    def __str__(self):
        return f'{self.number} | {self.balance} | {self.client}'
