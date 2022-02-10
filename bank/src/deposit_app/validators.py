from base_app.models import BankSettings

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_date(value):
    bank_settings, created = BankSettings.objects.get_or_create()

    if value < bank_settings.curr_bank_day:
        raise ValidationError(
            _('%(value)s is not correct! Specify date that\'s not in the past!'),
            params={'value': value},
        )
