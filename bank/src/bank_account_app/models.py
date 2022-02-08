from bank_account_app.choices import (BankAccountActivityTypeChoices,
                                      BankAccountTypeChoices)
from bank_account_app.mixins import ValidateCleanModelMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import validators


class BankAccount(ValidateCleanModelMixin, models.Model):
    '''Bank account model.
    Detailed information about bank accounts.
    Client has null value only in one case: if bank_account_type is BankAccountTypeChoices.SPECIAL
    '''

    number = models.CharField(
        'Number',
        max_length=13,
        unique=True,
        validators=[RegexValidator(
            regex='^[0-9]{13}$',
            message='Incorrect number'
        )]
    )
    activity_type = models.CharField('Activity type', choices=BankAccountActivityTypeChoices.choices, max_length=128)
    bank_account_type = models.CharField('Type', choices=BankAccountTypeChoices.choices, max_length=128)
    balance = models.DecimalField(
        'Balance',
        max_digits=21,
        decimal_places=2
    )
    client = models.ForeignKey(
        'client_app.Client',
        verbose_name='Client',
        on_delete=models.RESTRICT,
        related_name='bank_accounts',
        null=True
    )

    class Meta:
        ordering = ['number']
        verbose_name = 'Bank account'
        verbose_name_plural = 'Bank accounts'

    def __str__(self):
        return f'{self.number} | {self.balance} | {self.client} | {self.bank_account_type} | {self.activity_type}'

    def clean(self):
        errors = {}
        # Check if bank account has client (if bank account is not special fund)
        if (self.client is None) and (self.bank_account_type != BankAccountTypeChoices.SPECIAL):
            errors['client'] = _('Client can\'t be null!')
        if errors:
            raise validators.ValidationError(errors)
