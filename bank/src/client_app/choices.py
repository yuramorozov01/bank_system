from django.db import models
from django.utils.translation import gettext_lazy as _


class SexChoices(models.TextChoices):
    MALE = 'Male', _('Male')
    FEMALE = 'Female', _('Female')
    X = 'X', _('X')
    __empty__ = _('Unknown')


class CityChoices(models.TextChoices):
    MINSK = 'Minsk', _('Minsk')
    MOGILEV = 'Mogilev', _('Mogilev')
    VITEBSK = 'Vitebsk', _('Vitebsk')
    GOMEL = 'Gomel', _('Gomel')
    BREST = 'Brest', _('Brest')
    MOSCOW = 'Moscow', _('Moscow')
    WARSAWA = 'Warsawa', _('Warsawa')
    KYIV = 'Kyiv', _('Kyiv')
    VILNIUS = 'Vilnius', ('Vilnius')
    __empty__ = _('Unknown')


class FamilyStatusChoices(models.TextChoices):
    MARRIED = 'Married', _('Married')
    SINGLENESS = 'Singleness', _('Singleness')
    DIVORCED = 'Divorced', _('Divorced')
    COMMONLAW = 'Common-law', _('Common-law')
    __empty__ = _('Unknown')


class CitizenChoices(models.TextChoices):
    BELARUS = 'Belarus', _('Belarus')
    RUSSIA = 'Russian', _('Russian')
    UKRAINE = 'Ukraine', _('Ukraine')
    POLAND = 'Poland', _('Poland')
    LITHUANIA = 'Lithuania', _('Lithuania')
    __empty__ = _('Unknown')


class DisabilityChoices(models.IntegerChoices):
    GROUP_0 = 0, _('Group 0')
    GROUP_1 = 1, _('Group 1')
    GROUP_2 = 2, _('Group 2')
    GROUP_3 = 3, _('Group 3')
    __empty__ = _('Unknown')


class PassportSeriesChoices(models.TextChoices):
    AB = 'AB', _('AB')
    BM = 'BM', _('BM')
    HB = 'HB', _('HB')
    KH = 'KH', _('KH')
    MP = 'MP', _('MP')
    MC = 'MC', _('MC')
    KB = 'KB', _('KB')
    PP = 'PP', _('PP')
    SP = 'SP', _('SP')
    DP = 'DP', _('DP')
