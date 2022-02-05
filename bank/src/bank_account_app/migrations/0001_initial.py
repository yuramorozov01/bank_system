# Generated by Django 4.0.1 on 2022-02-05 14:39

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client_app', '0004_alter_client_monthly_salary'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=13, unique=True, validators=[django.core.validators.RegexValidator(message='Incorrect number', regex='^[0-9]{13}$')], verbose_name='Number')),
                ('activity_type', models.CharField(choices=[('Active', 'Active'), ('Passive', 'Passive'), ('ActivePassive', 'ActivePassive')], max_length=128, verbose_name='Activity type')),
                ('bank_account_type', models.CharField(choices=[('Main', 'Main'), ('Deposit', 'Deposit'), ('Credit', 'Credit'), ('Special', 'Special')], max_length=128, verbose_name='Type')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=13, verbose_name='Balance')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='bank_accounts', to='client_app.client', verbose_name='Client')),
            ],
            options={
                'verbose_name': 'Bank account',
                'verbose_name_plural': 'Bank accounts',
                'ordering': ['number'],
            },
        ),
    ]
