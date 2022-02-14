from django.db import models
from django.utils.translation import gettext_lazy as _


class CurrencyChoices(models.TextChoices):
    BYN = 'BYN', _('BYN')
    USD = 'USD', _('USD')
    EUR = 'EUR', _('EUR')
    RUB = 'RUB', _('RUB')
