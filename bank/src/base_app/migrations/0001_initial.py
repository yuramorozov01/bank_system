# Generated by Django 4.0.1 on 2022-02-07 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankSettings',
            fields=[
                ('settings_name', models.CharField(default='bank.settings', max_length=128, primary_key=True, serialize=False, verbose_name='Settings name')),
                ('curr_bank_day', models.DateField(auto_now_add=True, verbose_name='Current bank day')),
            ],
            options={
                'verbose_name': 'Bank settings',
                'verbose_name_plural': 'Bank settings',
            },
        ),
    ]
