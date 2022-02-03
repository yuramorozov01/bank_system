from django.db import models
from django.utils.translation import gettext_lazy as _


class BankAccountActivityTypeChoices(models.TextChoices):
    ACTIVE = 'Active', _('Active')
    PASSIVE = 'Passive', _('Passive')
    ACTIVE_PASSIVE = 'ActivePassive', _('ActivePassive')


class BankAccountTypeChoices(models.TextChoices):
    MAIN = 'Main', _('Main')
    DEPOSIT = 'Deposit', _('Deposit')
    CREDIT = 'Credit', _('Credit')
    SPECIAL = 'Special', _('Special')
