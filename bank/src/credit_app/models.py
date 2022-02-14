from base_app.choices import CurrencyChoices
from base_app.validators import validate_date_on_future
from django.core.validators import MinValueValidator
from django.db import models


class CreditType(models.Model):
    '''Credit type model.
    Detailed information about credit types.
    '''

    name = models.CharField('Name', max_length=128)
    percent = models.FloatField('Percent')
    credit_term = models.IntegerField('Credit term', validators=[MinValueValidator(0)])
    currency = models.CharField('Currency', choices=CurrencyChoices.choices, max_length=5)
    min_downpayment = models.DecimalField(
        'Minimal downpayment',
        max_digits=21,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    max_downpayment = models.DecimalField(
        'Maximum downpayment',
        max_digits=21,
        decimal_places=2,
        null=True,
        validators=[MinValueValidator(0)]
    )
    is_annuity_payment = models.BooleanField('Is annuity payment')

    class Meta:
        ordering = ['percent']
        verbose_name = 'Credit type'
        verbose_name_plural = 'Credit types'

    def __str__(self):
        return f'{self.name} | {self.percent} | {self.credit_term} | {self.currency}'


class CreditContract(models.Model):
    '''Credit contract model.
    Detailed information about credit contracts.
    '''

    credit_type = models.ForeignKey(
        CreditType,
        verbose_name='Credit type',
        on_delete=models.RESTRICT,
        related_name='contracts'
    )
    starts_at = models.DateField('Start date', validators=[validate_date_on_future])
    ends_at = models.DateField('End date', validators=[validate_date_on_future])
    is_ended = models.BooleanField('Is credit ended', default=False)
    credit_amount = models.DecimalField(
        'Credit amount',
        max_digits=21,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    client = models.ForeignKey(
        'client_app.Client',
        verbose_name='Client',
        on_delete=models.RESTRICT,
        related_name='credit_contracts'
    )
    main_bank_account = models.ForeignKey(
        'bank_account_app.BankAccount',
        verbose_name='Main bank account',
        on_delete=models.RESTRICT,
        related_name='credit_contracts_main'
    )
    credit_bank_account = models.ForeignKey(
        'bank_account_app.BankAccount',
        verbose_name='Credit bank account',
        on_delete=models.RESTRICT,
        related_name='credit_contracts_credit'
    )
    special_bank_account = models.ForeignKey(
        'bank_account_app.BankAccount',
        verbose_name='Special bank account',
        on_delete=models.RESTRICT,
        related_name='credit_contracts_special'
    )

    class Meta:
        ordering = ['starts_at']
        verbose_name = 'Credit contract'
        verbose_name_plural = 'Credit contract'

    def __str__(self):
        return f'{self.starts_at} - {self.ends_at} | ({self.client}) | {self.credit_amount}'
