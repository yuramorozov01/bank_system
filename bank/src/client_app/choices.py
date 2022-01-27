from django.db import models
from django.utils.translation import gettext_lazy as _


class SexChoices(models.TextChoices):
    MALE = 'ML', _('Male')
    FEMALE = 'FM', _('Female')
    X = 'X', _('X')
    __empty__ = _('Unknown')


class CityChoices(models.TextChoices):
    MINSK = 'MINSK', _('Minsk')
    MOGILEV = 'MOGILEV', _('Mogilev')
    VITEBSK = 'VITEBSK', _('Vitebsk')
    GOMEL = 'GOMEL', _('Gomel')
    BREST = 'BREST', _('Brest')
    MOSCOW = 'MOSCOW', _('Moscow')
    WARSAWA = 'WARSAWA', _('Warsawa')
    KYIV = 'KYIV', _('Kyiv')
    VILNIUS = 'VILNIUS', ('Vilnius')
    __empty__ = _('Unknown')


class FamilyStatusChoices(models.TextChoices):
    MARRIED = 'MR', _('Married')
    SINGLENESS = 'SG', _('Singleness')
    DIVORCED = 'DV', _('Divorced')
    COMMONLAW = 'CL', _('Common-law')
    __empty__ = _('Unknown')


class CitizenChoices(models.TextChoices):
    BELARUS = 'BLR', _('Belarus')
    RUSSIA = 'RUS', _('Russian')
    UKRAINE = 'UKR', _('Ukraine')
    POLAND = 'PLN', _('Poland')
    LITHUANIA = 'LTU', _('Lithuania')
    __empty__ = _('Unknown')


class DisabilityChoices(models.IntegerChoices):
    GROUP_0 = 0, _('Group 0')
    GROUP_1 = 1, _('Group 1')
    GROUP_2 = 2, _('Group 2')
    GROUP_3 = 3, _('Group 3')
    __empty__ = _('Unknown')
