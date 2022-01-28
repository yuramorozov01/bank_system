from django.db import models
from client_app.choices import SexChoices, CityChoices, FamilyStatusChoices, CitizenChoices, DisabilityChoices


class Client(models.Model):
    '''Client model.
    Detailed information about bank clients.
    '''

    last_name = models.CharField('Last name', max_length=128)
    first_name = models.CharField('First name', max_length=128)
    patronymic = models.CharField('Patronymic', max_length=128)

    birthday = models.DateField('Birthday')
    birthday_place = models.CharField('Birthday place', max_length=128)
    sex = models.CharField('Sex', choices=SexChoices.choices, max_length=32)

    passport_series = models.CharField('Passport series', max_length=8)
    passport_number = models.CharField('Passport number', max_length=64, unique=True)
    passport_issued_by = models.CharField('Passport issuer', max_length=128)
    passport_issued_at = models.DateField('Passport issue date')
    id_number = models.CharField('Identification number', max_length=128, unique=True)

    city = models.CharField('City', choices=CityChoices.choices, max_length=128)
    address = models.CharField('Address', max_length=256)

    home_number = models.CharField('Home number', max_length=32, null=True)
    phone_number = models.CharField('Phone number', max_length=32, null=True)

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
    monthly_salary = models.DecimalField('Monthly salary', max_digits=8, decimal_places=2, null=True)
    army = models.BooleanField('Liable for military service')

    class Meta:
        ordering = ['last_name']
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic} ({self.birthday})'
