from django.core.validators import RegexValidator
from django.db import models


class BankCard(models.Model):
    '''Bank card model.
    Detailed information about bank cards.
    '''

    number = models.CharField(
        'Number',
        max_length=16,
        unique=True,
        validators=[RegexValidator(
            regex='^[0-9]{16}$',
            message='Incorrect bank card number'
        )]
    )
    pin = models.CharField('PIN', max_length=128)
    bank_account = models.ForeignKey(
        'bank_account_app.BankAccount',
        verbose_name='Bank account',
        on_delete=models.CASCADE,
        related_name='bank_cards'
    )

    class Meta:
        ordering = ['number']
        verbose_name = 'Bank card'
        verbose_name_plural = 'Bank card'

    def __str__(self):
        return f'{self.number} | {self.bank_account}'
