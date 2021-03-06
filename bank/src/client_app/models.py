from client_app.choices import (CitizenChoices, CityChoices, DisabilityChoices,
                                FamilyStatusChoices, PassportSeriesChoices,
                                SexChoices)
from client_app.validators import validate_date
from django.core.validators import RegexValidator
from django.db import models


class Client(models.Model):
    '''Client model.
    Detailed information about bank clients.
    '''

    last_name = models.CharField('Last name', max_length=128, validators=[RegexValidator(
        regex=r'^[a-zA-Zа-яА-Я]+[a-zA-Zа-яА-Я-]+[a-zA-Zа-яА-Я]+$',
        message='Incorrect last name'
    )])
    first_name = models.CharField('First name', max_length=128, validators=[RegexValidator(
        regex=r'^[a-zA-Zа-яА-Я]+[a-zA-Zа-яА-Я-]+[a-zA-Zа-яА-Я]+$',
        message='Incorrect first name'
    )])
    patronymic = models.CharField('Patronymic', max_length=128, validators=[RegexValidator(
        regex=r'^[a-zA-Zа-яА-Я]+[a-zA-Zа-яА-Я-]+[a-zA-Zа-яА-Я]+$',
        message='Incorrect patronymic'
    )])

    birthday = models.DateField('Birthday', validators=[validate_date])
    birthday_place = models.CharField('Birthday place', max_length=128, validators=[RegexValidator(
        regex=r'^[a-zA-Zа-яА-Я]+[a-zA-Zа-яА-Я-]+[a-zA-Zа-яА-Я]+$',
        message='Incorrect birthday place'
    )])
    sex = models.CharField('Sex', choices=SexChoices.choices, max_length=32)

    passport_series = models.CharField('Passport series', choices=PassportSeriesChoices.choices, max_length=8)
    passport_number = models.CharField('Passport number', max_length=64, validators=[RegexValidator(
        regex=r'^[0-9]{7}$',
        message='Incorrect passport number'
    )])
    passport_issued_by = models.CharField('Passport issuer', max_length=128)
    passport_issued_at = models.DateField('Passport issue date', validators=[validate_date])
    id_number = models.CharField('Identification number', max_length=128, unique=True, validators=[RegexValidator(
        regex=r'^[0-9]{7}[аАвВсСкКеЕмМнН][0-9]{3}(PB|BA|BI)[0-9]$',
        message='Incorrect ID number'
    )])

    city = models.CharField('City', choices=CityChoices.choices, max_length=128)
    address = models.CharField('Address', max_length=256)

    home_number = models.CharField('Home number', max_length=32, null=True, validators=[RegexValidator(
        regex=r'^[0-9]{7}$',
        message='Incorrect home number'
    )])
    phone_number = models.CharField('Phone number', max_length=32, null=True, validators=[RegexValidator(
        regex=r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$',
        message='Incorrect phone number'
    )])

    email = models.EmailField('Email', max_length=254, null=True)

    job_place = models.CharField('Job place', max_length=128, null=True)
    job_position = models.CharField('Job position', max_length=256, null=True)

    register_city = models.CharField('Registration city', choices=CityChoices.choices, max_length=128)
    register_address = models.CharField('Registration address', max_length=256)

    family_status = models.CharField('Family status', choices=FamilyStatusChoices.choices, max_length=32)
    citizen = models.CharField('Citizen', choices=CitizenChoices.choices, max_length=128)
    disability = models.IntegerField(
        'Disability group',
        choices=DisabilityChoices.choices
    )
    pensioner = models.BooleanField('Pensioner')
    monthly_salary = models.DecimalField('Monthly salary', max_digits=13, decimal_places=2, null=True)
    army = models.BooleanField('Liable for military service')

    class Meta:
        ordering = ['last_name']
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        unique_together = ['passport_series', 'passport_number']

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic} ({self.birthday})'
