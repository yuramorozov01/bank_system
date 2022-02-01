from django.db import models
from django.core.validators import RegexValidator, MinValueValidator

from deposit_app.choices import (CurrencyChoices)
from deposit_app.validators import validate_date


class DepositType(models.Model):
    '''Deposit type model.
    Detailed information about deposit types.
    '''

    name = models.CharField('Name', max_length=128)
    percent = models.FloatField('Percent')
    deposit_term = models.IntegerField('Deposit term', validators=[MinValueValidator(0)])
    currency = models.CharField('Currency', choices=CurrencyChoices.choices, max_length=5)
    min_downpayment = models.DecimalField(
        'Minimal downpayment',
        max_digits=13,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    max_downpayment = models.DecimalField(
        'Maximum downpayment',
        max_digits=13,
        decimal_places=2,
        null=True,
        validators=[MinValueValidator(0)]
    )
    is_revocable = models.BooleanField('Is revocable')

    class Meta:
        ordering = ['-percent']
        verbose_name = 'Deposit type'
        verbose_name_plural = 'Deposit types'

    def __str__(self):
        return f'{self.name} | {self.percent} | {self.deposit_term} | {self.currency}'


class DepositContract(models.Model):
    '''Deposit contract model.
    Detailed information about deposit contracts.
    '''

    deposit_type = models.ForeignKey(
        DepositType,
        verbose_name='Deposit type',
        on_delete=models.RESTRICT,
        related_name='contracts'
    )
    starts_at = models.DateField('Start date', validators=[validate_date])
    ends_at = models.DateField('End date', validators=[validate_date])
    deposit_amount = models.DecimalField(
        'Deposit amount',
        max_digits=13,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    client = models.ForeignKey(
        'client_app.Client',
        verbose_name='Client',
        on_delete=models.RESTRICT,
        related_name='contracts'
    )

    class Meta:
        ordering = ['starts_at']
        verbose_name = 'Deposit contract'
        verbose_name_plural = 'Deposit contract'

    def __str__(self):
        return f'{self.starts_at} - {self.ends_at} | ({self.client}) | {self.deposit_amount}'
